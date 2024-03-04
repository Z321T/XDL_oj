import pandas as pd

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from administrator_app.models import Administrator, AdminNotification, ProgrammingExercise
from teacher_app.models import Teacher


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

    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    return render(request, 'home_administrator.html', {'dropdown_menu1': dropdown_menu1})


# 通知界面
def notice_administrator(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted').distinct()
    return render(request, 'notice_administrator.html',
                  {'dropdown_menu1': dropdown_menu1, 'adminnotifications': adminnotifications})


# 通知界面：发布通知
def create_notice(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('message')
        if title and content:
            adminnotification = AdminNotification.objects.create(
                title=title,
                content=content,
            )
            adminnotification.save()
            return redirect('administrator_app:notice_administrator')
    return render(request, 'create_notice_admin.html',
                  {'dropdown_menu1': dropdown_menu1})


# 通知界面：删除通知
def delete_notice(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        try:
            notification = AdminNotification.objects.filter(id=notification_id).first()
            notification.delete()
            return JsonResponse({'status': 'success'})
        except AdminNotification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '通知未找到'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=400)


# 通知界面：通知内容
def notification_content(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        notification = AdminNotification.objects.get(id=notification_id)
        return JsonResponse({'title': notification.title, 'content': notification.content})
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=400)


# 程序设计题库
def repository_administrator(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    programming_exercises = ProgrammingExercise.objects.all().order_by('-date_posted')

    context = {
        'dropdown_menu1': dropdown_menu1,
        'programming_exercises': programming_exercises,
    }
    return render(request, 'repository_administrator.html', context)


# 程序设计题库：添加程序设计题
def programmingexercise_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('content')
        deadline = request.POST.get('deadline')
        posted_by = request.session.get('user_id')

        if title and description and deadline and posted_by:
            ProgrammingExercise.objects.create(
                title=title,
                description=description,
                deadline=deadline,
                posted_by=Administrator.objects.get(userid=posted_by)
            )
            return redirect('administrator_app:repository_administrator')
    return render(request, 'programmingexercise_create.html')


# 程序设计题库：删除程序设计题
def programmingexercise_delete(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        if exercise_id:
            exercise_to_delete = ProgrammingExercise.objects.filter(id=exercise_id)
            exercise_to_delete.delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '练习未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=400)


# 管理员个人中心
def profile_administrator(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    administrator = Administrator.objects.get(userid=request.session.get('user_id'))

    context = {
        'dropdown_menu1': dropdown_menu1,
        'administrator': administrator,
    }
    return render(request, 'profile_administrator.html', context)


# 管理员个人中心：修改个人信息
def profile_administrator_edit(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    administrator = Administrator.objects.get(userid=request.session.get('user_id'))

    context = {
        'dropdown_menu1': dropdown_menu1,
        'administrator': administrator,
    }

    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        email = request.POST.get('email')
        administrator.phone_num = phone_num
        administrator.email = email
        administrator.save()
        return redirect('administrator_app:profile_administrator')

    return render(request, 'profile_administrator_edit.html', context)


# 题库查重管理
def problems_administrator(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    return render(request, 'problems_administrator.html', {'dropdown_menu1': dropdown_menu1})


# 教师管理
def information_administrator(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    teachers = Teacher.objects.all()
    return render(request, 'information_administrator.html',
                  {'dropdown_menu1': dropdown_menu1, 'teachers': teachers})


# 教师管理：添加教师
def add_teacher(request):
    if request.method == 'POST':
        initial_password = request.POST.get('initialPassword')
        file = request.FILES.get('excelFile')

        if initial_password and file:
            data = pd.read_excel(file)
            for index, row in data.iterrows():
                Teacher.objects.create(
                    name=row['姓名'],
                    userid=row['教工号'],
                    password=initial_password,
                )
            return redirect('administrator_app:information_administrator')
    return render(request, 'add_teacher.html')


# 教师管理：删除教师
def delete_teacher(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            classes_to_delete = teacher.classes_assigned.all()
            if classes_to_delete:
                for _class in classes_to_delete:
                    _class.delete()
            teacher.delete()
            return JsonResponse({'status': 'success', 'message': '教师及其相关班级删除成功'}, status=200)
        except Teacher.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '教师未找到'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=400)
