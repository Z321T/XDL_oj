import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from student_app.models import Student
from teacher_app.models import Teacher, Class, Notification, Exercise, Exam
from .forms import StudentForm

import subprocess


# 学生主页
def home_student(request):
    # 获取用户id，判断是否是学生用户，若不是则返回登录页面
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('/login/')
    try:
        student = Student.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        return redirect('/login/')

    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')

    return render(request, 'home_student.html',
                  {'dropdown_menu1': dropdown_menu1, 'notifications': notifications})


# 我的练习
def practice_student(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    student = Student.objects.get(userid=request.session.get('user_id'))
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')
    class_assigned = student.class_assigned
    exercises = Exercise.objects.filter(classes=class_assigned).order_by('-published_at')
    return render(request, 'practice_student.html',
                  {'dropdown_menu1': dropdown_menu1, 'exercises': exercises, 'notifications': notifications})


# 我的练习：练习详情
def practice_list(request, exercise_id):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    student = Student.objects.get(userid=request.session.get('user_id'))
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')
    if request.method == 'GET':
        exercise = Exercise.objects.get(id=exercise_id)
        return render(request, 'practice_list.html',
                      {'dropdown_menu1': dropdown_menu1, 'exercise': exercise, 'notifications': notifications})


# 我的考试
def test_student(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    student = Student.objects.get(userid=request.session.get('user_id'))
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')
    class_assigned = student.class_assigned
    exams = Exam.objects.filter(classes=class_assigned).order_by('-published_at')
    return render(request, 'test_student.html',
                  {'dropdown_menu1': dropdown_menu1, 'exams': exams, 'notifications': notifications})


# 我的考试：考试详情
def text_list(request, exam_id):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    student = Student.objects.get(userid=request.session.get('user_id'))
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')
    if request.method == 'GET':
        exam = Exam.objects.get(id=exam_id)
        return render(request, 'text_list.html',
                      {'dropdown_menu1': dropdown_menu1, 'exam': exam, 'notifications': notifications})


# 学生个人中心
def profile_student(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    student = Student.objects.get(userid=request.session.get('user_id'))
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile_student')
        else:
            # 如果表单无效，将错误信息返回到模板
            return render(request, 'profile_student.html',
                          {'form': form, 'dropdown_menu1': dropdown_menu1, 'notifications': notifications})
    else:
        form = StudentForm(instance=student)
    return render(request, 'profile_student.html',
                  {'form': form, 'dropdown_menu1': dropdown_menu1, 'notifications': notifications})


# 通知内容
def notification_content(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        notification = Notification.objects.get(id=notification_id)
        return JsonResponse({'title': notification.title, 'content': notification.content})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 答题界面
def coding_student(request):
    return render(request, 'coding_student.html')


def run_node_script(request):
    result = subprocess.run(['node', 'path_to_your_node_script.js'], capture_output=True, text=True)
    return result.stdout


def submit_code_view(request):
    # 这里处理提交的代码
    # 例如，你可以使用 request.POST.get('code') 来获取提交的代码
    return HttpResponse("代码已提交")
