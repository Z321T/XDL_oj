from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from app01.models import Student, Teacher, Administrators

# Create your views here.
def log_in(request):
    if request.method == 'POST':
        # 获取表单提交的用户名和密码
        username = request.POST['studentID']
        password = request.POST['password']

        # 使用Django的authenticate函数验证用户,根据用户类型选择相应的认证方式
        user = None
        if Student.objects.filter(student_id=username).exists():
            user = authenticate(request, student_id=username, password=password)
        elif Teacher.objects.filter(teacher_id=username).exists():
            user = authenticate(request, teacher_id=username, password=password)
        elif Administrators.objects.filter(teacher_id=username).exists():
            user = authenticate(request, admin_id=username, password=password)

        if user is not None:
            # 用户验证成功，登录用户
            login(request, user)
            return redirect('home')  # 重定向到登录后的首页，你需要替换 'home' 为你实际的URL
        else:
            # 用户验证失败，显示错误消息
            messages.error(request, '用户名或密码不正确')

    return render(request, "log_in.html")
