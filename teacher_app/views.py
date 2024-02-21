import pandas as pd
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from teacher_app.forms import TeacherForm, ClassForm
from teacher_app.models import Teacher, Class, Notification, Exercise, ExerciseQuestion, Exam, ExamQuestion
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


# 通知界面
def notice_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }

    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = teacher.classes_assigned.all()
    notifications = Notification.objects.filter(recipients__in=classes).order_by('-date_posted').distinct()
    return render(request, 'notice_teacher.html',
                  {'dropdown_menu1': dropdown_menu1, 'notifications': notifications})


# 发布通知
def create_notice(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = Class.objects.filter(teacher=teacher)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('message')
        recipient_ids = request.POST.get('recipients').split(',')
        recipients = Class.objects.filter(id__in=recipient_ids)

        if title and content and recipients:
            notification = Notification(title=title, content=content)
            notification.save()
            notification.recipients.set(recipients)
        return redirect('teacher_app:notice_teacher')
    return render(request, 'create_notice.html',
                  {'dropdown_menu1': dropdown_menu1, 'classes': classes})


# 删除通知
def delete_notice(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        if notification_id:
            notification_to_delete = Notification.objects.filter(id=notification_id).first()
            if notification_to_delete:
                notification_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '通知未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


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
            return redirect('teacher_app:profile_teacher')
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
    exercises = Exercise.objects.filter(teacher=teacher).order_by('-published_at')
    exams = Exam.objects.filter(teacher=teacher).order_by('-published_at')

    return render(request, 'repository_teacher.html',
                  {'dropdown_menu1': dropdown_menu1, 'exercises': exercises, 'exams': exams})


# 题库管理：练习列表
def exercise_list_default(request):
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = teacher.classes_assigned.all()

    exercise = Exercise.objects.create(
        title="默认标题",
        content="默认内容",
        deadline=datetime.now() + timedelta(days=7),
        teacher=teacher
    )

    return render(request, 'exercise_list.html',
                  {'classes': classes, 'exercise': exercise})


def exercise_list(request, exercise_id):
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = teacher.classes_assigned.all()
    exercise = get_object_or_404(Exercise, id=exercise_id)

    if request.method == 'POST':
        exercise.title = request.POST.get('title')
        exercise.content = request.POST.get('content')
        exercise.published_at = datetime.now()
        exercise.deadline = request.POST.get('deadline')

        recipient_ids = request.POST.get('recipients').split(',')
        recipient_class = Class.objects.filter(id__in=recipient_ids)
        if recipient_class:
            exercise.save()
            exercise.classes.set(recipient_class)
            return redirect('teacher_app:repository_teacher')
    return render(request, 'exercise_list.html',
                  {'classes': classes, 'exercise': exercise})


# 题库管理：练习列表-创建练习
def create_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        memory_limit = request.POST.get('memory_limit')
        time_limit = request.POST.get('time_limit')

        question = ExerciseQuestion(exercise=exercise, title=title, content=content,
                                    memory_limit=memory_limit, time_limit=time_limit)
        question.save()

        return redirect('teacher_app:exercise_list', exercise_id=exercise.id)
    return render(request, 'create_exercise.html', {'exercise': exercise})


# 题库管理：练习列表-修改练习题
def exercise_edit(request, exercise_id):
    if request.method == 'GET':
        exercise = Exercise.objects.get(id=exercise_id)
        return render(request, 'exercise_edit.html', {'exercise': exercise})


# 题库管理：练习列表-删除练习
def exercise_delete(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        if exercise_id:
            exercise_to_delete = Exercise.objects.filter(id=exercise_id).first()
            if exercise_to_delete:
                exercise_to_delete.questions.all().delete()
                exercise_to_delete.classes.clear()
                exercise_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '练习未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 题库管理：练习列表-删除练习题
def exercisequestion_delete(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        if question_id:
            question_to_delete = ExerciseQuestion.objects.filter(id=question_id).first()
            if question_to_delete:
                question_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '练习题未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 题库管理：考试列表
def exam_list_default(request):
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = teacher.classes_assigned.all()

    exam = Exam.objects.create(
        title="默认标题",
        content="默认内容",
        deadline=datetime.now() + timedelta(days=7),
        teacher=teacher
    )

    return render(request, 'exam_list.html',
                  {'classes': classes, 'exam': exam})


def exam_list(request, exam_id):
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = teacher.classes_assigned.all()
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        exam.title = request.POST.get('title')
        exam.content = request.POST.get('content')
        exam.published_at = datetime.now()
        exam.deadline = request.POST.get('deadline')

        recipient_ids = request.POST.get('recipients').split(',')
        recipient_class = Class.objects.filter(id__in=recipient_ids)
        if recipient_class:
            exam.save()
            exam.classes.set(recipient_class)
            return redirect('teacher_app:repository_teacher')
    return render(request, 'exam_list.html',
                  {'classes': classes, 'exam': exam})


# 题库管理：考试列表-创建考试
def create_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        memory_limit = request.POST.get('memory_limit')
        time_limit = request.POST.get('time_limit')

        question = ExamQuestion(exam=exam, title=title, content=content,
                                memory_limit=memory_limit, time_limit=time_limit)
        question.save()

        return redirect('teacher_app:exam_list', exam_id=exam.id)
    return render(request, 'create_exam.html', {'exam': exam})


# 题库管理：考试列表-修改考试题
def exam_edit(request, exam_id):
    if request.method == 'GET':
        exam = Exam.objects.get(id=exam_id)
        return render(request, 'exam_edit.html', {'exam': exam})


# 题库管理：考试列表-删除考试
def exam_delete(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        if exam_id:
            exam_to_delete = Exam.objects.filter(id=exam_id).first()
            if exam_to_delete:
                exam_to_delete.questions.all().delete()
                exam_to_delete.classes.clear()
                exam_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '考试未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 题库管理：考试列表-删除考试题
def examquestion_delete(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        if question_id:
            question_to_delete = ExamQuestion.objects.filter(id=question_id).first()
            if question_to_delete:
                question_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '考试题未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 作业情况
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
    classes = Class.objects.filter(teacher=teacher)
    return render(request, 'class_teacher.html',
                  {'classes': classes, 'dropdown_menu1': dropdown_menu1})


# 班级管理：创建班级
def create_class(request):
    if request.method == 'POST':
        class_name = request.POST.get('className')
        initial_password = request.POST.get('initialPassword')
        file = request.FILES.get('excelFile')

        if class_name and initial_password and file:
            teacher = Teacher.objects.get(userid=request.session.get('user_id'))
            new_class = Class.objects.create(name=class_name, teacher=teacher)
            teacher.classes_assigned.add(new_class)

            data = pd.read_excel(file)
            for index, row in data.iterrows():
                Student.objects.create(
                    name=row['姓名'],
                    userid=row['学号'],
                    password=initial_password,
                    class_assigned=new_class
                )
            return redirect('teacher_app:class_teacher')
    return render(request, 'create_class.html')


# 班级管理：删除班级
def delete_class(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        if class_id:
            class_to_delete = Class.objects.filter(id=class_id).first()
            if class_to_delete:
                for teacher in class_to_delete.teacher_set.all():
                    teacher.classes_assigned.remove(class_to_delete)
                class_to_delete.delete()
                return JsonResponse({'status': 'success', 'message': '班级删除成功'}, status=200)
        return JsonResponse({'status': 'error', 'message': '班级未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 班级管理：班级详情
def class_details(request, class_id):
    if request.method == 'GET':
        try:
            students = Student.objects.filter(class_assigned=class_id)
            return render(request, 'class_details.html', {'students': students})
        except Class.DoesNotExist:
            return redirect('teacher_app:class_teacher')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('teacher_app:class_teacher')


# 班级管理：删除学生
def delete_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student_to_delete = Student.objects.get(id=student_id)
            student_to_delete.class_assigned = None
            student_to_delete.save()
            student_to_delete.delete()
            return JsonResponse({'status': 'success', 'message': '删除成功'})
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '学生用户不存在'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


# 班级管理：初始化密码
def reset_password(request):
    if request.method == 'POST':
        student = Student.objects.get(id=request.POST.get('student_id'))
        try:
            student.password = 'cumt1909'  # 设置为默认密码
            student.save()
            return JsonResponse({'status': 'success', 'message': '初始化成功，密码改为cumt1909'}, status=200)
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '初始化密码失败'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
