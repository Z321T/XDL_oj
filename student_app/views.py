from django.shortcuts import render, redirect

from django.contrib import messages
from student_app.models import Student
from teacher_app.models import Teacher
from administrator_app.models import Administrator
from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request, "home_student.html")


