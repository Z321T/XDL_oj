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
    return render(request, 'home_student.html')


def practice_student(request):
    return render(request, 'practice_student.html')


def test_student(request):
    return render(request, 'test_student.html')


def profile_student(request):
    user_name = request.session.get('user_id')  # 获取用户名
    try:
        student = Student.objects.get(name=user_name)
    except ObjectDoesNotExist:
        messages.error(request, 'Student does not exist')
        return redirect('login')  # replace 'login' with the name of your login view

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('home_student')
        else:
            # 如果表单无效，将错误信息返回到模板
            return render(request, 'profile_student.html', {'form': form})
    else:
        form = StudentForm(instance=student)
    return render(request, 'profile_student.html', {'form': form})




