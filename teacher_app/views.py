from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages

from teacher_app.forms import TeacherForm
from teacher_app.models import Teacher


# Create your views here.
def home_teacher(request):
    # 获取用户id，若没有登录则返回登录页面
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('/login/')
    try:
        teacher = Teacher.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        messages.error(request, 'The teacher information is incorrect. Please log in again.')
        return redirect('/login/')

    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'home_teacher.html', {'dropdown_menu1': dropdown_menu1})


def notice_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'notice_teacher.html', {'dropdown_menu1': dropdown_menu1})


def profile_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }

    user_id = request.session.get('user_id')  # 获取用户
    try:
        teacher = Teacher.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Teacher does not exist')
        return redirect('/login/')  # replace 'login' with the name of your login view
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile_teacher')
        else:
            # 如果表单无效，将错误信息返回到模板
            return render(request, 'profile_teacher.html', {'form': form, 'dropdown_menu1': dropdown_menu1})
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'profile_teacher.html', {'form': form, 'dropdown_menu1': dropdown_menu1})


def repository_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'repository_teacher.html', {'dropdown_menu1': dropdown_menu1})


def test_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'test_teacher.html', {'dropdown_menu1': dropdown_menu1})


def class_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'class_teacher.html', {'dropdown_menu1': dropdown_menu1})
