import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from student_app.models import Student
from teacher_app.models import Teacher, Class, Notification, Exercise, Exam
from .forms import StudentForm


# 学生主页
def home_student(request):
    # 获取用户id，判断是否是学生用户，若不是则返回登录页面
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('/login/')
    try:
        student = Student.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        messages.error(request, 'The student information is incorrect. Please log in again.')
        return redirect('/login/')

    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }

    if request.method == 'GET':
        # 获取与学生关联的班级的所有通知，按照发布日期降序排序
        notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')

    return render(request, 'home_student.html',
                  {'dropdown_menu1': dropdown_menu1, 'notifications': notifications})


# 我的练习
def practice_student(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    student = Student.objects.get(userid=request.session.get('user_id'))
    class_assigned = student.class_assigned
    exercises = Exercise.objects.filter(classes=class_assigned).order_by('-published_at')
    return render(request, 'practice_student.html',
                  {'dropdown_menu1': dropdown_menu1, 'exercises': exercises})


# 我的练习：练习详情
def practice_list(request, exercise_id):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    # student = Student.objects.get(userid=request.session.get('user_id'))
    if request.method == 'GET':
        exercise = Exercise.objects.get(id=exercise_id)
        return render(request, 'practice_list.html',
                      {'dropdown_menu1': dropdown_menu1, 'exercise': exercise})


# 我的考试
def test_student(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    student = Student.objects.get(userid=request.session.get('user_id'))
    class_assigned = student.class_assigned
    exams = Exam.objects.filter(classes=class_assigned).order_by('-published_at')
    return render(request, 'test_student.html',
                  {'dropdown_menu1': dropdown_menu1, 'exams': exams})


# 我的考试：考试详情
def text_list(request, exam_id):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    # student = Student.objects.get(userid=request.session.get('user_id'))
    if request.method == 'GET':
        exam = Exam.objects.get(id=exam_id)
        return render(request, 'text_list.html',
                    {'dropdown_menu1': dropdown_menu1, 'exam': exam})

    # class_assigned = student.class_assigned
    # exams = Exam.objects.filter(classes=class_assigned).order_by('-published_at')
    # return render(request, 'test_student.html',
    #               {'dropdown_menu1': dropdown_menu1, 'exams': exams})


# 学生个人中心
def profile_student(request):

    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    student = Student.objects.get(userid=request.session.get('user_id'))
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile_student')
        else:
            # 如果表单无效，将错误信息返回到模板
            return render(request, 'profile_student.html', {'form': form, 'dropdown_menu1': dropdown_menu1})
    else:
        form = StudentForm(instance=student)
    return render(request, 'profile_student.html', {'form': form, 'dropdown_menu1': dropdown_menu1})


# 答题界面
def coding_student(request):
    return render(request, 'coding_student.html')


# 接受通知
# def notifications_view(request):
#     user_id = request.session.get('user_id')
#     student = Student.objects.get(userid=user_id)
#     if request.method == 'GET':
#         # 获取与学生关联的班级的所有通知，按照发布日期降序排序
#         notifications = Notification.objects.filter(recipients__in=student.classes.all()).order_by('-date_posted')
#         # 将通知传递给模板，并渲染模板
#         return render(request, 'home_student.html', {'notifications': notifications})

