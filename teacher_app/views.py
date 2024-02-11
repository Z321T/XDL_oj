from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from student_app.models import Student
from teacher_app.models import Teacher, Class, Announcement
from .forms import TeacherForm


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

    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('/login/')
    try:
        teacher = Teacher.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        messages.error(request, 'The teacher information is incorrect. Please log in again.')
        return redirect('/login/')
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


# 处理发布公告的视图函数
def send_announcement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        class_id = request.POST.get('class_id')
        published_at = timezone.now().date()

        teacher = Teacher.objects.get(userid=request.session.get('user_id'))  # 获取当前登录的教师
        class_to_notify = Class.objects.get(id=class_id)

        students = Student.objects.filter(class_assigned=class_to_notify)
        announcement = Announcement(title=title, content=content, published_at=published_at,
                                    teacher=teacher, class_to_notify=class_to_notify)
        announcement.save()
        announcement.students.set(students)
        return JsonResponse({'message': 'Announcement sent successfully.'})
    else:
        return render(request, 'send_announcement.html')