import os
import json
import time
import requests
import subprocess

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse

from administrator_app.models import ProgrammingExercise
from student_app.models import (Student, Score, ExerciseCompletion, ExerciseQuestionCompletion,
                                ExamCompletion, ExamQuestionCompletion)
from teacher_app.models import Notification, Exercise, Exam, ExerciseQuestion, ExamQuestion
from CodeBERT_app.views import analyze_code, analyze_programming_code
from .forms import StudentForm


# 学生主页
def home_student(request):
    # 获取用户id，判断是否是学生用户，若不是则返回登录页面
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('/login/')
    try:
        student = Student.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        return redirect('/login/')

    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')
    programing_exercises = ProgrammingExercise.objects.all().order_by('-date_posted')

    context = {
        'dropdown_menu1': dropdown_menu1,
        'notifications': notifications,
        'programing_exercises': programing_exercises,
    }

    return render(request, 'home_student.html', context)


# 学生主页：提交报告
def report_student(request, programmingexercise_id):
    programing_exercise = ProgrammingExercise.objects.get(id=programmingexercise_id)
    if request.method == 'GET':
        return render(request, 'report_student.html', {'programing_exercise': programing_exercise})


# 我的练习
def practice_student(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    student = Student.objects.get(userid=request.session.get('user_id'))
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')
    class_assigned = student.class_assigned
    exercises = Exercise.objects.filter(classes=class_assigned).order_by('-published_at')
    return render(request, 'practice_student.html',
                  {'dropdown_menu1': dropdown_menu1, 'exercises': exercises, 'notifications': notifications})


# 我的练习：练习详情
def practice_list(request, exercise_id):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    student = Student.objects.get(userid=request.session.get('user_id'))
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')
    if request.method == 'GET':
        exercise = Exercise.objects.get(id=exercise_id)
        return render(request, 'practice_list.html',
                      {'dropdown_menu1': dropdown_menu1, 'exercise': exercise, 'notifications': notifications})


# 我的考试
def test_student(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    student = Student.objects.get(userid=request.session.get('user_id'))
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')
    class_assigned = student.class_assigned
    exams = Exam.objects.filter(classes=class_assigned).order_by('-published_at')
    return render(request, 'test_student.html',
                  {'dropdown_menu1': dropdown_menu1, 'exams': exams, 'notifications': notifications})


# 我的考试：考试详情
def text_list(request, exam_id):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    student = Student.objects.get(userid=request.session.get('user_id'))
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')
    if request.method == 'GET':
        exam = Exam.objects.get(id=exam_id)
        return render(request, 'text_list.html',
                      {'dropdown_menu1': dropdown_menu1, 'exam': exam, 'notifications': notifications})


# 学情分析
def analyse_student(request):
    student = Student.objects.get(userid=request.session.get('user_id'))
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')

    context = {
        'dropdown_menu1': dropdown_menu1,
        'notifications': notifications,
    }
    return render(request, 'analyse_student.html', context)


# 学生个人中心
def profile_student(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    student = Student.objects.get(userid=request.session.get('user_id'))
    notifications = Notification.objects.filter(recipients=student.class_assigned).order_by('-date_posted')
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile_student')
        else:
            # 如果表单无效，将错误信息返回到模板
            return render(request, 'profile_student.html',
                          {'form': form, 'dropdown_menu1': dropdown_menu1, 'notifications': notifications})
    else:
        form = StudentForm(instance=student)
    return render(request, 'profile_student.html',
                  {'form': form, 'dropdown_menu1': dropdown_menu1, 'notifications': notifications})


# 通知内容
def notification_content(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        notification = Notification.objects.get(id=notification_id)
        return JsonResponse({'title': notification.title, 'content': notification.content})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 答题界面
def coding_exercise(request, exercisequestion_id):
    if request.method == 'GET':
        question = get_object_or_404(ExerciseQuestion, id=exercisequestion_id)
        question_set = question.exercise
        types = 'exercise'
        return render(request, 'coding_student.html',
                      {'question_set': question_set, 'question': question, 'types': types})
    return render(request, 'coding_student.html')


def coding_exam(request, examquestion_id):
    if request.method == 'GET':
        question = get_object_or_404(ExamQuestion, id=examquestion_id)
        question_set = question.exam
        types = 'exam'
        return render(request, 'coding_student.html',
                      {'question_set': question_set, 'question': question, 'types': types})
    return render(request, 'coding_student.html')


def call_node_api(request):
    response = requests.get('http://localhost:3000/api')  # Node.js服务器的地址
    return HttpResponse(response.json())


# 标记完成的题目
def mark_exercise_question_as_completed(student, exercise_question):
    ExerciseQuestionCompletion.objects.create(
        student=student,
        exercise_question=exercise_question,
        completed_at=timezone.now()
    )
    # 检查是否所有的练习题都已经完成
    all_questions = exercise_question.exercise.questions.all()
    completed_questions = ExerciseQuestionCompletion.objects.filter(
        student=student,
        exercise_question__in=all_questions
    )
    if all_questions.count() == completed_questions.count():
        ExerciseCompletion.objects.create(
            student=student,
            exercise=exercise_question.exercise,
            completed_at=timezone.now()
        )


def mark_exam_question_as_completed(student, exam_question):
    ExamQuestionCompletion.objects.create(
        student=student,
        exam_question=exam_question,
        completed_at=timezone.now()
    )
    all_questions = exam_question.exam.questions.all()
    completed_questions = ExamQuestionCompletion.objects.filter(
        student=student,
        exam_question__in=all_questions
    )
    if all_questions.count() == completed_questions.count():
        ExamCompletion.objects.create(
            student=student,
            exam=exam_question.exam,
            completed_at=timezone.now()
        )


# 运行C++代码
def run_cpp_code(request):
    student = Student.objects.get(userid=request.session.get('user_id'))
    if request.method == 'POST':
        user_code = request.POST.get('code', '')  # 从表单数据中获取代码
        types = request.POST.get('types', '')  # 从表单数据中获取题目类型
        question_id = request.POST.get('questionId', '')  # 从表单数据中获取题目id

        with open('temp.cpp', 'w') as f:
            f.write(user_code)

        try:
            start_time = time.time()  # 记录开始时间
            result = subprocess.run(
                ['docker', 'run', '--rm', '-v', f"{os.getcwd()}:/app",
                 '-w', '/app', '-m', '512m', '--cpus', '1', 'cpp-runner',
                 'bash', '-c', 'g++ temp.cpp -o temp && ./temp'],
                capture_output=True, text=True, timeout=30
            )
            execution_time = time.time() - start_time  # 计算执行时间

            if result.returncode == 0:  # 如果运行成功
                if types == 'exercise':
                    question = ExerciseQuestion.objects.get(id=question_id)
                else:
                    question = ExamQuestion.objects.get(id=question_id)
                if question.answer == result.stdout:
                    if types == 'exercise':
                        mark_exercise_question_as_completed(student, question)
                        Score.objects.create(
                            student=student,
                            exercise_question=question,
                            score=10
                        )
                    else:
                        mark_exam_question_as_completed(student, question)
                        Score.objects.create(
                            student=student,
                            exam_question=question,
                            score=10
                        )
                    analyze_code(student, user_code, types, question_id)
                    # 这里仅返回了执行结果和时间，与前端代码对应
                    return JsonResponse({'output': result.stdout, 'time': execution_time})
                else:
                    return JsonResponse({'output': result.stdout, 'error': 'Wrong answer', 'time': execution_time})
            else:  # 如果编译或运行出错
                return JsonResponse({'error': result.stderr, 'time': execution_time})
        except subprocess.TimeoutExpired:  # 如果运行超时
            return JsonResponse({'error': 'Execution timed out'})
        except Exception as e:  # 如果发生其他异常
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)



