import json

from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from administrator_app.models import Administrator
from student_app.models import Student
from teacher_app.models import Teacher


# Create your views here.
@csrf_exempt  # 这里添加了csrf_exempt装饰器，因为Ajax请求可能不包含csrf令牌
def log_in(request):
    if request.method == 'POST':
        # 获取表单提交的用户名和密码
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # 使用Django的authenticate函数验证用户,根据用户类型选择相应的认证方式
        user = None
        user_type = None  # 添加用户类型变量

        if Student.objects.filter(student_id=username).exists():
            user = Student.objects.get(student_id=username)
            if password == user.password:
                user_type = 'student'
            else:
                user = None
            # user = authenticate(request, student_id=username, password=password)
            # user_type = 'student'
        elif Teacher.objects.filter(teacher_id=username).exists():
            user = Teacher.objects.get(teacher_id=username)
            if password == user.password:
                user_type = 'teacher'
            else:
                user = None
            # user = authenticate(request, teacher_id=username, password=password)
            # user_type = 'teacher'
        elif Administrator.objects.filter(admin_id=username).exists():
            user = Administrator.objects.get(admin_id=username)
            if password == user.password:
                user_type = 'administrator'
            else:
                user = None
            # user = authenticate(request, admin_id=username, password=password)
            # user_type = 'administrator'
        else:
            # 用户不存在，返回错误消息
            error_message = 'Username is incorrect'
            # messages.error(request, error_message)
            return JsonResponse({'status': 'error', 'message': error_message})

        if user is not None:
            # 用户验证成功，登录用户
            login(request, user)
            request.session['user_id'] = user.name  # 保存用户id
            return JsonResponse({'status': 'success', 'message': user_type})
        else:
            # 用户验证失败，显示不同的错误消息
            error_message = 'Password is incorrect'
            # messages.error(request, error_message)
            return JsonResponse({'status': 'error', 'message': error_message})

    return render(request, "log_in.html")
