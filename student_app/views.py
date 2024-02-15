import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from student_app.models import Student
from teacher_app.models import Teacher
from .forms import StudentForm




# Create your views here.
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
    return render(request, 'home_student.html', {'dropdown_menu1': dropdown_menu1})


# 我的练习
def practice_student(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'practice_student.html', {'dropdown_menu1': dropdown_menu1})


# 我的考试
def test_student(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'test_student.html', {'dropdown_menu1': dropdown_menu1})


# 学生个人中心
def profile_student(request):

    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }

    user_id = request.session.get('user_id')  # 获取用户
    try:
        student = Student.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Student does not exist')
        return redirect('/login/')
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

