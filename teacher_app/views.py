import pandas as pd

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

from teacher_app.forms import TeacherForm, ClassForm
from teacher_app.models import Teacher, Class, Notification, Exercise, ExerciseQuestion, Exam
from student_app.models import Student
from student_app.forms import StudentForm


# Create your views here.
# 教师主页
def home_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    # 获取用户id，若没有登录则返回登录页面
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('/login/')
    try:
        teacher = Teacher.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        messages.error(request, 'The teacher information is incorrect. Please log in again.')
        return redirect('/login/')
        # 这里我们不再需要单独的 dropdown_menu1，因为教师信息已经包含 user_id
        # 但是如果有其他数据需要传递给下拉菜单，你可以在这里添加

        # 假设这是你的饼状图数据
    chart_data = {
        'categories': ['分类1', '分类2', '分类3'],
        'data': [30, 50, 20]
    }
    # 你可以传递一个包含所有信息的上下文字典给模板
    # 这里是你的数据，通常是从数据库中查询得到的
    line_chart_data = {
        'dates': ['1', '2', '3', '4', '5'],
        'values': [120, 132, 101, 134, 90]
    }

    context = {
        'dropdown_menu1': dropdown_menu1,  # 添加 teacher 对象
        'chart_data': chart_data,  # 添加图表数据
        'line_chart_data': line_chart_data,  # 添加折线图数据
    }

    return render(request, 'home_teacher.html', context)


# 发布通知
def notice_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    user_id = request.session.get('user_id')
    teacher = Teacher.objects.get(userid=user_id)
    classes = Class.objects.filter(teacher=teacher)

    if request.method == 'POST':
        content = request.POST.get('message')
        recipient_ids = request.POST.getlist('recipients')
        recipients = Class.objects.filter(id__in=recipient_ids)

        if content and recipients:
            notification = Notification(content=content)
            notification.save()
            notification.recipients.set(recipients)
            messages.success(request, '通知已成功发送')
        else:
            messages.error(request, '发送通知失败')
        return redirect('teacher_app:notice_teacher')  # 重定向到你的视图URL
    return render(request, 'notice_teacher.html', {'dropdown_menu1': dropdown_menu1, 'classes': classes})


# 教师个人中心
def profile_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }

    user_id = request.session.get('user_id')
    teacher = Teacher.objects.get(userid=user_id)

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile_teacher')
        else:
            # 如果表单无效，将错误信息返回到模板
            return render(request, 'profile_teacher.html', {'form': form, 'dropdown_menu1': dropdown_menu1})
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'profile_teacher.html', {'form': form, 'dropdown_menu1': dropdown_menu1})


# 题库管理
def repository_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }

    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    exercises = Exercise.objects.filter(teacher=teacher)
    exams = Exam.objects.filter(teacher=teacher)

    return render(request, 'repository_teacher.html',
                  {'dropdown_menu1': dropdown_menu1, 'exercises': exercises, 'exams': exams})


# 创建练习
def create_exercise(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        deadline = request.POST.get('deadline')
        class_ids = request.POST.getlist('classes')
        classes = Class.objects.filter(id__in=class_ids)

        exercise = Exercise(title=title, content=content, deadline=deadline)
        exercise.teacher = Teacher.objects.get(userid=request.session.get('user_id'))
        exercise.save()
        exercise.classes.set(classes)

        return redirect('repository_teacher')
    return render(request, 'create_exercise.html')


# 创建考试
def create_exam(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        deadline = request.POST.get('deadline')
        class_ids = request.POST.getlist('classes')
        classes = Class.objects.filter(id__in=class_ids)

        exam = Exam(title=title, content=content, deadline=deadline)
        exam.teacher = Teacher.objects.get(userid=request.session.get('user_id'))
        exam.save()
        exam.classes.set(classes)

        return redirect('repository_teacher')
    return render(request, 'create_exam.html')


# 考试情况
def test_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'test_teacher.html', {'dropdown_menu1': dropdown_menu1})


# 班级管理
def class_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    # 查询与当前教师关联的班级
    classes = Class.objects.filter(teacher=teacher)
    return render(request, 'class_teacher.html',
                  {'classes': classes, 'dropdown_menu1': dropdown_menu1})


# 班级管理：创建班级
def create_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST, request.FILES)
        if form.is_valid():
            new_class = form.save(commit=False)
            class_name = request.POST.get('name')
            new_class.name = class_name

            teacher = Teacher.objects.get(userid=request.session.get('user_id'))
            new_class.teacher = teacher  # 将班级的教师设置为当前登录的教师
            new_class.save()
            teacher.classes_assigned.add(new_class)  # 然后将班级添加到教师的 classes_assigned 中

            file = request.FILES.get('file')
            if file:
                initial_password = request.POST.get('initialPassword')
                data = pd.read_excel(file)
                for index, row in data.iterrows():
                    Student.objects.create(
                        name=row['姓名'],
                        userid=row['学号'],
                        password=initial_password,
                        class_assigned=new_class
                    )
            return JsonResponse({'message': '班级创建成功'}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)


# 班级管理：删除班级
def delete_class(request):
    class_id = request.GET.get('nid')
    if class_id:
        class_to_delete = Class.objects.filter(id=class_id).first()
        if class_to_delete:
            for teacher in class_to_delete.teachers.all():
                teacher.classes_assigned.remove(class_to_delete)
            class_to_delete.delete()
    return redirect('class_teacher')


# 班级管理：获取学生信息
def get_students(request):
    students = Student.objects.filter(class_assigned=class_id)
    student_list = []
    for student in students:
        student_list.append({
            'id': student.id,
            'name': student.name,
            'userid': student.userid,
            'password': student.password,
            'email': student.email,
            'last_login': student.last_login
        })
    return JsonResponse({'students': student_list})


# 班级管理：删除学生
def delete_student(request, student_id):
    try:
        student_to_delete = Student.objects.get(id=student_id)
        student_to_delete.delete()
        messages.success(request, 'Student deleted successfully.')
    except Student.DoesNotExist:
        messages.error(request, 'The student does not exist')
    return redirect('class_teacher')


# 班级管理：初始化密码
def reset_password(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        student.password = 'default_password'  # 设置为默认密码
        student.save()
        messages.success(request, 'Password reset successfully.')
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')
    return redirect('class_teacher')
