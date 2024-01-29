from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from student_app.models import Student
from teacher_app.models import Teacher
from administrator_app.models import Administrator
from django.http import JsonResponse


# Create your views here.
def log_in(request):
    if request.method == 'POST':
        # 获取表单提交的用户名和密码
        username = request.POST['username']
        password = request.POST['password']

        # 使用Django的authenticate函数验证用户,根据用户类型选择相应的认证方式
        user = None
        user_type = None  # 添加用户类型变量

        if Student.objects.filter(student_id=username).exists():
            user = authenticate(request, student_id=username, password=password)
            user_type = 'student'
        elif Teacher.objects.filter(teacher_id=username).exists():
            user = authenticate(request, teacher_id=username, password=password)
            user_type = 'teacher'
        elif Administrator.objects.filter(teacher_id=username).exists():
            user = authenticate(request, admin_id=username, password=password)
            user_type = 'administrator'
        else:
            # 用户不存在，返回错误消息
            error_message = 'Username is incorrect'
            # messages.error(request, error_message)
            return JsonResponse({'status': 'error', 'message': error_message})

        if user is not None:
            # 用户验证成功，登录用户
            login(request, user)
            # 根据用户类型重定向到不同的主页
            return JsonResponse({'status': 'success', 'message': user_type})
        else:
            # 用户验证失败，显示不同的错误消息
            error_message = 'Password is incorrect'
            # messages.error(request, error_message)
            return JsonResponse({'status': 'error', 'message': error_message})

    return render(request, "log_in.html")


def home(request):
    return render(request, "home_student(origin).html")


