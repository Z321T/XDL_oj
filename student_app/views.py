import json
from django.shortcuts import render, redirect

from django.contrib import messages
from student_app.models import Student
from teacher_app.models import Teacher
from administrator_app.models import Administrator
from django.http import HttpResponse, JsonResponse
from .forms import StudentForm
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def home_student(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'home_student.html', {'dropdown_menu1': dropdown_menu1})


def practice_student(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'practice_student.html', {'dropdown_menu1': dropdown_menu1})


def test_student(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'test_student.html', {'dropdown_menu1': dropdown_menu1})


def profile_student(request):

    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }

    user_id = request.session.get('user_id')  # 获取用户
    try:
        student = Student.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Student does not exist')
        return redirect('/login/')  # replace 'login' with the name of your login view
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


def coding_student(request):
    return render(request, 'coding_student.html')


