from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from administrator_app.models import Administrator
from administrator_app.forms import AdministratorForm


# Create your views here.
# 管理员主页
def home_administrator(request):
    # 获取用户id，若没有登录则返回登录页面
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('/login/')
    try:
        administrator = Administrator.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        messages.error(request, 'The administrator information is incorrect. Please log in again.')
        return redirect('/login/')

    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'home_administrator.html', {'dropdown_menu1': dropdown_menu1})


# 发布通知
def notice_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'notice_administrator.html', {'dropdown_menu1': dropdown_menu1})


# 管理员个人中心
def profile_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }

    administrator = Administrator.objects.get(userid=request.session.get('user_id'))

    if request.method == 'POST':
        form = AdministratorForm(request.POST, instance=administrator)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile_administrator')
        else:
            messages.error(request, 'Profile update failed')
            return redirect('profile_administrator')
    else:
        form = AdministratorForm(instance=administrator)
    return render(request, 'profile_administrator.html', {'form': form, 'dropdown_menu1': dropdown_menu1})


# 我的题库
def repository_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'repository_administrator.html', {'dropdown_menu1': dropdown_menu1})


# 考试情况
def test_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'test_administrator.html', {'dropdown_menu1': dropdown_menu1})


# 班级管理
def class_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'class_administrator.html', {'dropdown_menu1': dropdown_menu1})


# 查重管理
def plagiarism_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'plagiarism_administrator.html', {'dropdown_menu1': dropdown_menu1})


# 师生信息管理
def information_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'information_administrator.html', {'dropdown_menu1': dropdown_menu1})


# 题库管理
def problems_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'problems_administrator.html', {'dropdown_menu1': dropdown_menu1})


