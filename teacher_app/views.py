import pandas as pd

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages

from teacher_app.forms import TeacherForm, ClassForm
from teacher_app.models import Teacher, Class
from student_app.models import Student
from student_app.forms import StudentForm


# Create your views here.
# 教师主页
def home_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    # 获取用户id，若没有登录则返回登录页面
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('/login/')
    try:
        teacher = Teacher.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        messages.error(request, 'The teacher information is incorrect. Please log in again.')
        return redirect('/login/')
        # 这里我们不再需要单独的 dropdown_menu1，因为教师信息已经包含 user_id
        # 但是如果有其他数据需要传递给下拉菜单，你可以在这里添加

        # 假设这是你的饼状图数据
    chart_data = {
        'categories': ['分类1', '分类2', '分类3'],
        'data': [30, 50, 20]
    }
    # 你可以传递一个包含所有信息的上下文字典给模板
    # 这里是你的数据，通常是从数据库中查询得到的
    line_chart_data = {
        'dates': ['1', '2', '3', '4', '5'],
        'values': [120, 132, 101, 134, 90]
    }

    context = {
        'dropdown_menu1': dropdown_menu1,  # 添加 teacher 对象
        'chart_data': chart_data,  # 添加图表数据
        'line_chart_data': line_chart_data,  # 添加折线图数据
    }

    return render(request, 'home_teacher.html', context)


# 发布通知
def notice_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'notice_teacher.html', {'dropdown_menu1': dropdown_menu1})


# 教师个人中心
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


# 题库管理
def repository_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'repository_teacher.html', {'dropdown_menu1': dropdown_menu1})


# 考试情况
def test_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'test_teacher.html', {'dropdown_menu1': dropdown_menu1})


# 班级管理
def class_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }

    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            new_class = form.save()
            # 读取Excel文件
            excel_file = request.FILES['excel_file']
            data = pd.read_excel(excel_file)
            # 创建学生用户
            for index, row in data.iterrows():
                Student.objects.create(
                    name=row['姓名'],
                    userid=row['学号'],
                    password=row['default_password'],
                    class_assigned=new_class
                )
            return redirect('class_teacher')
    else:
        form = ClassForm()

    classes = Class.objects.all()
    return render(request, 'class_teacher.html', {'form': form, 'classes': classes, 'dropdown_menu1': dropdown_menu1})


# 班级管理：删除班级
def delete_class(request, class_id):
    try:
        class_to_delete = Class.objects.get(id=class_id)
        class_to_delete.delete()
        messages.success(request, 'Class deleted successfully.')
    except Class.DoesNotExist:
        messages.error(request, 'The class does not exist')
        return redirect('class_teacher')


# 班级管理：删除学生
def delete_student(request, student_id):
    try:
        student_to_delete = Student.objects.get(id=student_id)
        student_to_delete.delete()
        messages.success(request, 'Student deleted successfully.')
    except Student.DoesNotExist:
        messages.error(request, 'The student does not exist')
    return redirect('class_teacher')


# 班级管理：初始化密码
def reset_password(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        student.password = 'default_password'  # 设置为默认密码
        student.save()
        messages.success(request, 'Password reset successfully.')
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')
    return redirect('class_teacher')
