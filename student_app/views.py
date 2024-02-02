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


