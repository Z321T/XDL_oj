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
