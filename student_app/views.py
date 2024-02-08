import json
from django.shortcuts import render, redirect

from django.contrib import messages
from student_app.models import Student
from teacher_app.models import Teacher
from administrator_app.models import Administrator
from django.http import JsonResponse


# Create your views here.
def home_student(request):
    return render(request, 'home_student.html')


def practice_student(request):
    return render(request, 'practice_student.html')


def test_student(request):
    return render(request, 'test_student.html')


def profile_student(request):
    return render(request, 'profile_student.html')
def coding_student(request):
    return render(request, 'coding_student.html')

def student_info(request):
    if request.method == 'GET':
        user_name = request.session.get('user_id')  # 获取用户名
        if user_name is not None:
            student = Student.objects.get(name=user_name)
            return JsonResponse({'name': student.name, 'student_id': student.student_id, 'class': student.class_num, 'email': student.email})

    elif request.method == 'POST':
        data = json.loads(request.body)
        user_name = request.session.get('user_id')  # 获取用户名
        student = Student.objects.get(name=user_name)
        student.name = data['name']
        student.student_id = data['student_id']
        student.class_num = data['class']
        student.email = data['email']
        student.save()
        return JsonResponse({'status': 'success'}, status=200)
