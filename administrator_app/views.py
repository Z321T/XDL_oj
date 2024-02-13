from django.shortcuts import render, redirect
from django.contrib import messages
from administrator_app.models import Administrator
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
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

def notice_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'notice_administrator.html', {'dropdown_menu1': dropdown_menu1})


def profile_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'profile_administrator.html', {'dropdown_menu1': dropdown_menu1})


def repository_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'repository_administrator.html', {'dropdown_menu1': dropdown_menu1})


def test_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'test_administrator.html', {'dropdown_menu1': dropdown_menu1})

def class_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'class_administrator.html', {'dropdown_menu1': dropdown_menu1})

def plagiarism_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'plagiarism_administrator.html', {'dropdown_menu1': dropdown_menu1})

def information_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'information_administrator.html', {'dropdown_menu1': dropdown_menu1})

def problems_administrator(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'problems_administrator.html', {'dropdown_menu1': dropdown_menu1})


