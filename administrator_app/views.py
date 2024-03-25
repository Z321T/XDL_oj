import os
import tempfile
import docx
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from CodeBERT_app.views import analyze_programming_report, analyze_programming_code
from administrator_app.models import Administrator, AdminNotification, ProgrammingExercise, AdminExam, AdminExamQuestion
from teacher_app.models import Teacher, Class
from student_app.models import Student, Score
from CodeBERT_app.models import ReportStandardScore
from login.views import check_login


# 管理员主页-程序设计
def home_administrator(request):
    # 获取用户id，若没有登录则返回登录页面
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    programings = ProgrammingExercise.objects.all().order_by('-date_posted')

    context = {
        'user_id': user_id,
        'coursework': programings,
    }
    return render(request, 'home_administrator.html', context)


# 管理员主页-考试
def home_administrator_exam(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')
    
    AdminExam.objects.filter(title="默认标题").delete()
    exams = AdminExam.objects.all().order_by('-published_at')

    context = {
        'user_id': user_id,
        'coursework': exams,
    }
    return render(request, 'home_administrator_exam.html', context)


# 程序设计题详情
def programmingexercise_details_data(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    if request.method == 'POST':
        question_id = request.POST.get('id')
        try:
            question = ProgrammingExercise.objects.get(id=question_id)
            total_students = Student.objects.count()
            total_submissions = ReportStandardScore.objects.filter(programming_question=question).count()
            ratio = total_submissions / total_students if total_students else 0
            ratio_data = [{
                'completion_rate': ratio,
            }]

            context = {
                'ratio_data': ratio_data,
            }
            return JsonResponse({'data': context})

        except ProgrammingExercise.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '未找到对应的练习题'}, status=404)

    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=400)


# 考试题详情
def exam_details_data(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    if request.method == 'POST':
        exam_id = request.POST.get('id')
        try:
            exam = AdminExam.objects.get(id=exam_id)
            questions = exam.questions.all()
            question_avg_scores = []

            for question in questions:
                # 获取当前题目所有分数对象
                scores = Score.objects.filter(adminexam_question=question)
                total_score = sum(score.score for score in scores)
                total_students = Student.objects.count()
                # 计算平均分，若学生总数为0，则平均分为0
                avg_score = (total_score / total_students) if total_students else 0

                question_avg_scores.append({
                    'question_title': question.title,
                    'average_score': avg_score
                })

            return JsonResponse({'data': question_avg_scores})

        except AdminExam.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '未找到对应的考试'}, status=404)

    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=400)


# 程序设计题库
def repository_administrator(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    programming_exercises = ProgrammingExercise.objects.all().order_by('-date_posted')

    context = {
        'user_id': user_id,
        'programming_exercises': programming_exercises,
    }
    return render(request, 'repository_administrator.html', context)


# 程序设计题库：添加程序设计题
def programmingexercise_create(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

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
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        if exercise_id:
            exercise_to_delete = ProgrammingExercise.objects.filter(id=exercise_id)
            exercise_to_delete.delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '练习未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=400)


# 题库查重管理
def problems_administrator(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    programming_exercises = ProgrammingExercise.objects.all().order_by('-date_posted')

    context = {
        'user_id': user_id,
        'programming_exercises': programming_exercises,
    }
    return render(request, 'problems_administrator.html', context)


# 题库查重管理-导入数据
def report_administrator(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    programmingexercise_id = request.GET.get('exerciseId')

    if request.method == 'POST':
        student = None
        word_file = request.FILES['wordFile']

        if word_file:
            # 读取文件内容并使用BytesIO创建一个类似文件的对象
            word_file_bytes = BytesIO(word_file.read())
            # 使用BytesIO对象创建docx文档对象
            document = docx.Document(word_file_bytes)
            full_text = []
            for paragraph in document.paragraphs:
                full_text.append(paragraph.text)
            # 获得纯文本代码，去除了图片
            report = '\n'.join(full_text)
            # 分析报告特征
            analyze_programming_report(student, report, programmingexercise_id)

        # 读取TXT文件内容
        code_file = request.FILES.get('txtFile')
        if code_file:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
            temp_file.write(code_file.read())
            temp_file.close()
            # 分析代码特征
            code = open(temp_file.name, encoding='utf-8').read()
            analyze_programming_code(student, code, programmingexercise_id)
            os.unlink(temp_file.name)
        return JsonResponse({'status': 'success', 'message': '提交成功'})

    context = {
        'user_id': user_id,
    }
    return render(request, 'report_administrator.html', context)


# 考试
def exam_administrator(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    AdminExam.objects.filter(title="默认标题").delete()
    exams = AdminExam.objects.all().order_by('-published_at')

    context = {
        'user_id': user_id,
        'exams': exams,
    }
    return render(request, 'exam_administrator.html', context)


# 考试-考试列表
def admin_examlist_default(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    admin = Administrator.objects.get(userid=user_id)
    exam = AdminExam.objects.create(
        title="默认标题",
        content="默认内容",
        deadline=datetime.now() + timedelta(days=7),
        teacher=admin
    )

    return render(request, 'admin_examlist.html',
                  {'exam': exam})


def admin_examlist(request, exam_id):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    admin = Administrator.objects.get(userid=user_id)
    exam = get_object_or_404(AdminExam, id=exam_id)

    if request.method == 'POST':
        exam.title = request.POST.get('title')
        exam.content = request.POST.get('content')
        exam.published_at = datetime.now()
        exam.deadline = request.POST.get('deadline')

        recipient_class = Class.objects.all()
        if recipient_class:
            exam.save()
            exam.classes.set(recipient_class)
            return redirect('administrator_app:exam_administrator')
    return render(request, 'admin_examlist.html',
                  {'exam': exam})


# 考试-考试列表-创建考试
def create_adminexam(request, exam_id):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    exam = get_object_or_404(AdminExam, id=exam_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        memory_limit = request.POST.get('memory_limit')
        time_limit = request.POST.get('time_limit')
        answer = request.POST.get('answer')

        question = AdminExamQuestion(exam=exam, title=title, content=content,
                                     memory_limit=memory_limit, time_limit=time_limit, answer=answer)
        question.save()

        return redirect('administrator_app:admin_examlist', exam_id=exam.id)
    return render(request, 'create_adminexam.html', {'exam': exam})


# 考试-考试列表-修改考试题
def adminexam_edit(request, exam_id):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    if request.method == 'GET':
        exam = AdminExam.objects.get(id=exam_id)
        context = {
            'exam': exam,
            'user_id': user_id,
        }
        return render(request, 'adminexam_edit.html', context)


# 考试-考试列表-删除考试
def adminexam_delete(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        if exam_id:
            exam_to_delete = AdminExam.objects.filter(id=exam_id).first()
            if exam_to_delete:
                exam_to_delete.questions.all().delete()
                exam_to_delete.classes.clear()
                exam_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '考试未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 考试-考试列表-删除考试题
def adminexamquestion_delete(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        if question_id:
            question_to_delete = AdminExamQuestion.objects.filter(id=question_id).first()
            if question_to_delete:
                question_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '考试题未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 通知界面
def notice_administrator(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    adminnotifications = AdminNotification.objects.all().order_by('-date_posted').distinct()
    return render(request, 'notice_administrator.html',
                  {'user_id': user_id, 'adminnotifications': adminnotifications})


# 通知界面：发布通知
def create_notice(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

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
                  {'user_id': user_id})


# 通知界面：删除通知
def delete_notice(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

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
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        notification = AdminNotification.objects.get(id=notification_id)
        return JsonResponse({'title': notification.title, 'content': notification.content})
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=400)


# 教师管理
def information_administrator(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    teachers = Teacher.objects.all()
    return render(request, 'information_administrator.html',
                  {'user_id': user_id, 'teachers': teachers})


# 教师管理：添加教师
def add_teacher(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    if request.method == 'POST':
        initial_password = request.POST.get('initialPassword')
        file = request.FILES.get('excelFile')

        if initial_password and file:
            data = pd.read_excel(file)
            for index, row in data.iterrows():
                hashed_password = make_password(initial_password)
                Teacher.objects.create(
                    name=row['姓名'],
                    userid=row['教工号'],
                    password=hashed_password,
                )
            return redirect('administrator_app:information_administrator')
    return render(request, 'add_teacher.html')


# 教师管理：删除教师
def delete_teacher(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

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


# 教师管理：重置密码
def reset_password(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    if request.method == 'POST':
        teacher = Teacher.objects.get(id=request.POST.get('teacher_id'))
        try:
            initial_password = 'cumt1909'  # 设置为默认密码
            hashed_password = make_password(initial_password)
            teacher.password = hashed_password
            teacher.save()
            return JsonResponse({'status': 'success', 'message': '初始化成功，密码改为cumt1909'}, status=200)
        except Teacher.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '初始化密码失败'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


# 管理员个人中心
def profile_administrator(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    administrator = Administrator.objects.get(userid=request.session.get('user_id'))

    context = {
        'user_id': user_id,
        'administrator': administrator,
    }
    return render(request, 'profile_administrator.html', context)


# 管理员个人中心：修改个人信息
def profile_administrator_edit(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    administrator = Administrator.objects.get(userid=request.session.get('user_id'))

    context = {
        'user_id': user_id,
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


# 管理员个人中心-修改密码
def profile_adminadministrator_password(request):
    user_id = request.session.get('user_id')
    if check_login(user_id):
        return redirect('/login/')

    administrator = Administrator.objects.get(userid=user_id)

    context = {
        'user_id': user_id,
    }

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if check_password(old_password, administrator.password):
            if new_password == confirm_password:
                administrator.password = make_password(new_password)
                administrator.save()
                return JsonResponse({'status': 'success', 'message': '密码修改成功'})
            else:
                return JsonResponse({'status': 'error', 'message': '两次输入的密码不一致'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': '旧密码错误'}, status=400)

    return render(request, 'password_admin_edit.html', context)



