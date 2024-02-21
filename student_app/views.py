import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from student_app.models import Student
from teacher_app.models import Teacher, Class, Notification, Exercise, Exam
from .forms import StudentForm

import json
import time
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests


# 学生主页
def home_student(request):
    # 获取用户id，判断是否是学生用户，若不是则返回登录页面
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('/login/')
    try:
        student = Student.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        messages.error(request, 'The student information is incorrect. Please log in again.')
        return redirect('/login/')

    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }

    if request.method == 'GET':
        # 获取与学生关联的班级的所有通知，按照发布日期降序排序
        notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')

    return render(request, 'home_student.html',
                  {'dropdown_menu1': dropdown_menu1, 'notifications': notifications})


# 我的练习
def practice_student(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    student = Student.objects.get(userid=request.session.get('user_id'))
    class_assigned = student.class_assigned
    exercises = class_assigned.exercises.all()

    return render(request, 'practice_student.html', {'dropdown_menu1': dropdown_menu1})


# 我的考试
def test_student(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    student = Student.objects.get(userid=request.session.get('user_id'))
    class_assigned = student.class_assigned
    exams = Exam.objects.filter(classes=class_assigned)
    return render(request, 'test_student.html',
                  {'dropdown_menu1': dropdown_menu1, 'exams': exams})


# 学生个人中心
def profile_student(request):

    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    student = Student.objects.get(userid=request.session.get('user_id'))
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile_student')
        else:
            # 如果表单无效，将错误信息返回到模板
            return render(request, 'profile_student.html', {'form': form, 'dropdown_menu1': dropdown_menu1})
    else:
        form = StudentForm(instance=student)
    return render(request, 'profile_student.html', {'form': form, 'dropdown_menu1': dropdown_menu1})


# 答题界面
def coding_student(request):
    return render(request, 'coding_student.html')


# 接受通知
# def notifications_view(request):
#     user_id = request.session.get('user_id')
#     student = Student.objects.get(userid=user_id)
#     if request.method == 'GET':
#         # 获取与学生关联的班级的所有通知，按照发布日期降序排序
#         notifications = Notification.objects.filter(recipients__in=student.classes.all()).order_by('-date_posted')
#         # 将通知传递给模板，并渲染模板
#         return render(request, 'home_student.html', {'notifications': notifications})





def call_node_api(request):
    response = requests.get('http://localhost:3000/api')  # Node.js服务器的地址
    return HttpResponse(response.json())

@csrf_exempt  # 临时禁用 CSRF 保护，注意这在生产环境中可能是不安全的
def run_cpp_code(request):
    # 确保请求方法是 POST 并且内容类型是 JSON
    if request.method == 'POST' and request.content_type == 'application/json':
        data = json.loads(request.body.decode('utf-8'))  # 解析 JSON 数据
        user_code = data.get('code', '')

        with open('temp.cpp', 'w') as f:
            f.write(user_code)

        try:
            start_time = time.time()  # 记录开始时间

            result = subprocess.run(
                ['docker', 'run', '--rm', '-v', f"{os.getcwd()}:/app", '-w', '/app',
                 '-m', '512m', '--cpus', '1', 'cpp-runner',
                 'bash', '-c', 'g++ temp.cpp -o temp && ./temp'],
                capture_output=True, text=True, timeout=30
            )

            execution_time = time.time() - start_time  # 计算执行时间

            if result.returncode == 0:
                return JsonResponse({'output': result.stdout, 'time': execution_time})
            else:
                return JsonResponse({'error': result.stderr, 'time': execution_time})
        except subprocess.TimeoutExpired:
            return JsonResponse({'error': 'Execution timed out'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)