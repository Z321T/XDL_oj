import pandas as pd
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotFound

from CodeBERT_app.models import ProgrammingCodeFeature, ProgrammingReportFeature, CodeStandardScore
from CodeBERT_app.views import compute_cosine_similarity
from administrator_app.models import AdminNotification, ProgrammingExercise
from teacher_app.models import (Teacher, Class, Notification,
                                Exercise, ExerciseQuestion, Exam, ExamQuestion, ReportScore)
from student_app.models import (Student, ExerciseCompletion, ExamCompletion,
                                Score, ExerciseQuestionCompletion, ExamQuestionCompletion)


# Create your views here.
# 教师主页
def home_teacher(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    # 获取用户id，若没有登录则返回登录页面
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('/login/')
    try:
        teacher = Teacher.objects.get(userid=user_id)
    except ObjectDoesNotExist:
        return redirect('/login/')

    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    programing_exercises = ProgrammingExercise.objects.all().order_by('-date_posted')

    context = {
        'dropdown_menu1': dropdown_menu1,
        'adminnotifications': adminnotifications,
        'programing_exercises': programing_exercises
    }

    return render(request, 'home_teacher.html', context)


# 教师主页：查看报告
def repeat_report(request, programmingexercise_id):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    classes = Class.objects.filter(teacher=teacher)

    context = {
        'dropdown_menu1': dropdown_menu1,
        'adminnotifications': adminnotifications,
        'classes': classes,
        'programmingexercise_id': programmingexercise_id
    }
    return render(request, 'repeat_report.html', context)


# 教师主页：查看报告-获取文本数据
def repeat_report_details(request, programmingexercise_id):
    class_id = request.GET.get('class_id')
    students = Student.objects.filter(class_assigned=class_id)
    programmingexercise = ProgrammingExercise.objects.get(id=programmingexercise_id)
    student_similarities = []

    for student in students:
        # 尝试获取当前学生对于特定练习题的编程特征，否则为None
        try:
            student_feature = ProgrammingReportFeature.objects.get(student=student,
                                                                   programming_question=programmingexercise)
        except ProgrammingReportFeature.DoesNotExist:
            student_feature = None

        if student_feature:
            max_similarity = 0
            sim_student = None
            other_features = ProgrammingReportFeature.objects.filter(
                programming_question=programmingexercise).exclude(student=student)
            for other_feature_record in other_features:
                similarity = compute_cosine_similarity(student_feature.feature, other_feature_record.feature)
                if similarity > max_similarity:
                    max_similarity = similarity
                    sim_student = other_feature_record.student
            # 在列表中为当前学生存储最大相似度值和学生对象
            student_similarities.append((student, max_similarity, sim_student))
            # 更新或创建当前学生的余弦相似度记录
            ProgrammingReportFeature.objects.update_or_create(
                student=student,
                programming_question=programmingexercise,
                defaults={'cosine_similarity': max_similarity, 'similar_student': sim_student}
            )
        else:
            # 如果没有学生特征，我们将相似度设置为None
            student_similarities.append((student, None, None))

    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    classes = Class.objects.filter(teacher=teacher)

    context = {
        'dropdown_menu1': dropdown_menu1,
        'adminnotifications': adminnotifications,
        'classes': classes,
        'programmingexercise_id': programmingexercise_id,
        'students': students,
        'student_similarities': student_similarities,
    }
    return render(request, 'repeat_report_details.html', context)


# 教师主页：查看报告-获取代码数据
def repeat_code_details(request, programmingexercise_id):
    class_id = request.GET.get('class_id')
    students = Student.objects.filter(class_assigned=class_id)
    programmingexercise = ProgrammingExercise.objects.get(id=programmingexercise_id)
    student_similarities = []

    for student in students:
        # 尝试获取当前学生对于特定练习题的编程特征，否则为None
        try:
            student_feature = ProgrammingCodeFeature.objects.get(student=student,
                                                                 programming_question=programmingexercise)
        except ProgrammingCodeFeature.DoesNotExist:
            student_feature = None

        if student_feature:
            max_similarity = 0
            sim_student = None
            other_features = ProgrammingCodeFeature.objects.filter(
                programming_question=programmingexercise).exclude(student=student)
            for other_feature_record in other_features:
                similarity = compute_cosine_similarity(student_feature.feature, other_feature_record.feature)
                if similarity > max_similarity:
                    max_similarity = similarity
                    sim_student = other_feature_record.student
            # 在列表中为当前学生存储最大相似度值和学生对象
            student_similarities.append((student, max_similarity, sim_student))
            # 更新或创建当前学生的余弦相似度记录
            ProgrammingCodeFeature.objects.update_or_create(
                student=student,
                programming_question=programmingexercise,
                defaults={'cosine_similarity': max_similarity, 'similar_student': sim_student}
            )
        else:
            # 如果没有学生特征，我们将相似度设置为None
            student_similarities.append((student, None, None))

    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    classes = Class.objects.filter(teacher=teacher)

    context = {
        'dropdown_menu1': dropdown_menu1,
        'adminnotifications': adminnotifications,
        'classes': classes,
        'programmingexercise_id': programmingexercise_id,
        'students': students,
        'student_similarities': student_similarities,
    }
    return render(request, 'repeat_code_details.html', context)


# 教师主页-规范性评分
def standard_report(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    try:
        stand_score = ReportScore.objects.filter(teacher=teacher).first()
    except ObjectDoesNotExist:
        stand_score = None

    if stand_score:
        context = {
            'dropdown_menu1': dropdown_menu1,
            'adminnotifications': adminnotifications,
            'stand_score': stand_score,
        }
    else:
        context = {
            'dropdown_menu1': dropdown_menu1,
            'adminnotifications': adminnotifications,
        }
    if request.method == 'POST':
        totalscore = request.POST.get('totalscore')
        contents = request.POST.get('contents')
        firstrow = request.POST.get('firstrow')
        fontsize = request.POST.get('fontsize')
        image = request.POST.get('image')
        pagenum = request.POST.get('pagenum')

        ReportScore.objects.update_or_create(
            teacher=teacher,
            defaults={
                'totalscore': totalscore,
                'contents': contents,
                'firstrow': firstrow,
                'fontsize': fontsize,
                'image': image,
                'pagenum': pagenum,
            }
        )
        return redirect('teacher_app:standard_report')
    return render(request, 'standard_report.html', context)


# 教师主页-得分详情
def scores_details(request, programmingexercise_id, class_id):
    # 获取特定编程题目，班级所有学生的代码规范性得分
    students = Student.objects.filter(class_assigned=class_id)
    student_scores = []
    for student in students:
        try:
            score_instance = CodeStandardScore.objects.get(student=student, programming_question=programmingexercise_id)
            student_scores.append((student, score_instance.standard_score))
        except CodeStandardScore.DoesNotExist:
            student_scores.append((student, None))
    context = {
      'student_scores': student_scores,
      # ...其他context内容
    }
    return render(request, 'scores_details.html', context)


# 作业情况
def coursework_exercise(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    exercises = Exercise.objects.filter(teacher=teacher).order_by('-published_at')
    classes = teacher.classes_assigned.all()

    context = {
        'dropdown_menu1': dropdown_menu1,
        'coursework': exercises,
        'classes': classes,
        'adminnotifications': adminnotifications
    }

    return render(request, 'coursework_exercise.html', context)


def coursework_exam(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    exams = Exam.objects.filter(teacher=teacher).order_by('-published_at')
    classes = teacher.classes_assigned.all()

    context = {
        'dropdown_menu1': dropdown_menu1,
        'coursework': exams,
        'classes': classes,
        'adminnotifications': adminnotifications
    }

    return render(request, 'coursework_exam.html', context)


# 作业情况：获取数据
def coursework_data(request):
    if request.method == 'POST':
        data_type = request.POST.get('type')
        item_id = request.POST.get('id')
        response_data = []

        if data_type == 'exercise':
            exercise = get_object_or_404(Exercise, id=item_id)
            related_classes = exercise.classes.all()
        elif data_type == 'exam':
            exam = get_object_or_404(Exam, id=item_id)
            related_classes = exam.classes.all()
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data type'}, status=400)

        for class_group in related_classes:
            students = class_group.students.all()
            total_students = students.count()
            student_ids = students.values_list('id', flat=True)

            if total_students > 0:
                if data_type == 'exercise':
                    completed_count = ExerciseCompletion.objects.filter(exercise=exercise, student_id__in=student_ids).count()
                else:
                    completed_count = ExamCompletion.objects.filter(exam=exam, student_id__in=student_ids).count()

                completion_rate = (completed_count / total_students) * 100
                response_data.append({
                    'class_name': class_group.name,
                    'completion_rate': completion_rate
                })
            else:
                response_data.append({
                    'class_name': class_group.name,
                    'completion_rate': 0
                })

        return JsonResponse({'data': response_data})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 作业情况：练习详情
def coursework_exercise_details(request, class_id):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    if request.method == 'GET':
        try:
            class_item = Class.objects.get(id=class_id)
            exercises = Exercise.objects.filter(classes=class_item).order_by('-published_at')

            context = {
                'dropdown_menu1': dropdown_menu1,
                'coursework': exercises,
                'class_id': class_id,
                'adminnotifications': adminnotifications
            }
            return render(request, 'coursework_exercise_details.html', context)
        except (Class.DoesNotExist, Exercise.DoesNotExist) as e:
            return HttpResponseNotFound('所请求的数据不存在')


# 作业情况：考试详情
def coursework_exam_details(request, class_id):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    if request.method == 'GET':
        try:
            class_item = Class.objects.get(id=class_id)
            exams = Exam.objects.filter(classes=class_item).order_by('-published_at')

            context = {
                'dropdown_menu1': dropdown_menu1,
                'coursework': exams,
                'class_id': class_id,
                'adminnotifications': adminnotifications
            }
            return render(request, 'coursework_exam_details.html', context)
        except (Class.DoesNotExist, Exercise.DoesNotExist) as e:
            return HttpResponseNotFound('所请求的数据不存在')


# 作业情况-详情界面：获取数据
def coursework_details_data(request):
    if request.method == 'POST':
        data_type = request.POST.get('type')
        item_id = request.POST.get('id')
        class_item = get_object_or_404(Class, id=request.POST.get('class_id'))
        students = class_item.students.all()
        total_students = students.count()
        student_ids = students.values_list('id', flat=True)

        if data_type == 'exercise':
            exercise = get_object_or_404(Exercise, id=item_id)
            exercise_completed_count = ExerciseCompletion.objects.filter(exercise=exercise, student_id__in=student_ids).count()
            exercise_completion_rate = (exercise_completed_count / total_students) * 100 if total_students > 0 else 0
            exercise_data = [{
                'completion_rate': exercise_completion_rate
            }]

            questions = ExerciseQuestion.objects.filter(exercise=exercise)
            exercisequestion_data = []
            for question in questions:
                question_completed_count = ExerciseQuestionCompletion.objects.filter(exercise_question=question, student_id__in=student_ids).count()
                question_completion_rate = (question_completed_count / total_students) * 100 if total_students > 0 else 0
                exercisequestion_data.append({
                    'question_title': question.title,
                    'completion_rate': question_completion_rate
                })

            context = {
                'exercise_data': exercise_data,
                'exercisequestion_data': exercisequestion_data
            }
            return JsonResponse({'data': context})

        elif data_type == 'exam':
            exam = get_object_or_404(Exam, id=item_id)
            exam_completed_count = ExamCompletion.objects.filter(exam=exam, student_id__in=student_ids).count()
            exam_completion_rate = (exam_completed_count / total_students) * 100 if total_students > 0 else 0
            exam_data = [{
                'completion_rate': exam_completion_rate
            }]

            questions = ExamQuestion.objects.filter(exam=exam)
            examquestion_data = []
            for question in questions:
                question_completed_count = ExamQuestionCompletion.objects.filter(exam_question=question, student_id__in=student_ids).count()
                question_completion_rate = (question_completed_count / total_students) * 100 if total_students > 0 else 0
                examquestion_data.append({
                    'question_title': question.title,
                    'completion_rate': question_completion_rate
                })

            context = {
                'exam_data': exam_data,
                'examquestion_data': examquestion_data
            }
            return JsonResponse({'data': context})


# 题库管理
def repository_teacher(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')

    Exercise.objects.filter(title="默认标题").delete()
    Exam.objects.filter(title="默认标题").delete()
    exercises = Exercise.objects.filter(teacher=teacher).order_by('-published_at')
    exams = Exam.objects.filter(teacher=teacher).order_by('-published_at')

    context = {
        'dropdown_menu1': dropdown_menu1,
        'exercises': exercises,
        'exams': exams,
        'adminnotifications': adminnotifications
    }
    return render(request, 'repository_teacher.html', context)


# 题库管理：练习列表
def exercise_list_default(request):
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = teacher.classes_assigned.all()

    exercise = Exercise.objects.create(
        title="默认标题",
        content="默认内容",
        deadline=datetime.now() + timedelta(days=7),
        teacher=teacher
    )

    return render(request, 'exercise_list.html',
                  {'classes': classes, 'exercise': exercise})


def exercise_list(request, exercise_id):
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = teacher.classes_assigned.all()
    exercise = get_object_or_404(Exercise, id=exercise_id)

    if request.method == 'POST':
        exercise.title = request.POST.get('title')
        exercise.content = request.POST.get('content')
        exercise.published_at = datetime.now()
        exercise.deadline = request.POST.get('deadline')

        recipient_ids = request.POST.get('recipients').split(',')
        recipient_class = Class.objects.filter(id__in=recipient_ids)
        if recipient_class:
            exercise.save()
            exercise.classes.set(recipient_class)
            return redirect('teacher_app:repository_teacher')
    return render(request, 'exercise_list.html',
                  {'classes': classes, 'exercise': exercise})


# 题库管理：练习列表-创建练习
def create_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        memory_limit = request.POST.get('memory_limit')
        time_limit = request.POST.get('time_limit')
        answer = request.POST.get('answer')

        question = ExerciseQuestion(exercise=exercise, title=title, content=content,
                                    memory_limit=memory_limit, time_limit=time_limit, answer=answer)
        question.save()

        return redirect('teacher_app:exercise_list', exercise_id=exercise.id)
    return render(request, 'create_exercise.html', {'exercise': exercise})


# 题库管理：练习列表-修改练习题
def exercise_edit(request, exercise_id):
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    if request.method == 'GET':
        exercise = Exercise.objects.get(id=exercise_id)
        context = {
            'exercise': exercise,
            'adminnotifications': adminnotifications
        }
        return render(request, 'exercise_edit.html', context)


# 题库管理：练习列表-删除练习
def exercise_delete(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        if exercise_id:
            exercise_to_delete = Exercise.objects.filter(id=exercise_id).first()
            if exercise_to_delete:
                exercise_to_delete.questions.all().delete()
                exercise_to_delete.classes.clear()
                exercise_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '练习未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 题库管理：练习列表-删除练习题
def exercisequestion_delete(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        if question_id:
            question_to_delete = ExerciseQuestion.objects.filter(id=question_id).first()
            if question_to_delete:
                question_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '练习题未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 题库管理：考试列表
def exam_list_default(request):
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = teacher.classes_assigned.all()

    exam = Exam.objects.create(
        title="默认标题",
        content="默认内容",
        deadline=datetime.now() + timedelta(days=7),
        teacher=teacher
    )

    return render(request, 'exam_list.html',
                  {'classes': classes, 'exam': exam})


def exam_list(request, exam_id):
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = teacher.classes_assigned.all()
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        exam.title = request.POST.get('title')
        exam.content = request.POST.get('content')
        exam.published_at = datetime.now()
        exam.deadline = request.POST.get('deadline')

        recipient_ids = request.POST.get('recipients').split(',')
        recipient_class = Class.objects.filter(id__in=recipient_ids)
        if recipient_class:
            exam.save()
            exam.classes.set(recipient_class)
            return redirect('teacher_app:repository_teacher')
    return render(request, 'exam_list.html',
                  {'classes': classes, 'exam': exam})


# 题库管理：考试列表-创建考试
def create_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        memory_limit = request.POST.get('memory_limit')
        time_limit = request.POST.get('time_limit')
        answer = request.POST.get('answer')

        question = ExamQuestion(exam=exam, title=title, content=content,
                                memory_limit=memory_limit, time_limit=time_limit, answer=answer)
        question.save()

        return redirect('teacher_app:exam_list', exam_id=exam.id)
    return render(request, 'create_exam.html', {'exam': exam})


# 题库管理：考试列表-修改考试题
def exam_edit(request, exam_id):
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    if request.method == 'GET':
        exam = Exam.objects.get(id=exam_id)
        context = {
            'exam': exam,
            'adminnotifications': adminnotifications
        }
        return render(request, 'exam_edit.html', context)


# 题库管理：考试列表-删除考试
def exam_delete(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        if exam_id:
            exam_to_delete = Exam.objects.filter(id=exam_id).first()
            if exam_to_delete:
                exam_to_delete.questions.all().delete()
                exam_to_delete.classes.clear()
                exam_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '考试未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 题库管理：考试列表-删除考试题
def examquestion_delete(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        if question_id:
            question_to_delete = ExamQuestion.objects.filter(id=question_id).first()
            if question_to_delete:
                question_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '考试题未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 通知界面
def notice_teacher(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    classes = teacher.classes_assigned.all()
    notifications = Notification.objects.filter(recipients__in=classes).order_by('-date_posted').distinct()

    context = {
        'dropdown_menu1': dropdown_menu1,
        'notifications': notifications,
        'adminnotifications': adminnotifications
    }
    return render(request, 'notice_teacher.html', context)


# 发布通知
def create_notice(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = Class.objects.filter(teacher=teacher)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('message')
        recipient_ids = request.POST.get('recipients').split(',')
        recipients = Class.objects.filter(id__in=recipient_ids)

        if title and content and recipients:
            notification = Notification(title=title, content=content)
            notification.save()
            notification.recipients.set(recipients)
        return redirect('teacher_app:notice_teacher')
    return render(request, 'create_notice.html',
                  {'dropdown_menu1': dropdown_menu1, 'classes': classes})


# 删除通知
def delete_notice(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        if notification_id:
            notification_to_delete = Notification.objects.filter(id=notification_id).first()
            if notification_to_delete:
                notification_to_delete.delete()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': '通知未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=400)


# 通知详情
def notification_content(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        notification = Notification.objects.get(id=notification_id)
        return JsonResponse({'title': notification.title, 'content': notification.content})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 班级管理
def class_teacher(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    classes = Class.objects.filter(teacher=teacher)

    context = {
        'classes': classes,
        'dropdown_menu1': dropdown_menu1,
        'adminnotifications': adminnotifications
    }
    return render(request, 'class_teacher.html', context)


# 班级管理：创建班级
def create_class(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    context = {
        'dropdown_menu1': dropdown_menu1,
        'adminnotifications': adminnotifications
    }
    if request.method == 'POST':
        class_name = request.POST.get('className')
        initial_password = request.POST.get('initialPassword')
        file = request.FILES.get('excelFile')

        if class_name and initial_password and file:
            teacher = Teacher.objects.get(userid=request.session.get('user_id'))
            new_class = Class.objects.create(name=class_name, teacher=teacher)
            teacher.classes_assigned.add(new_class)

            data = pd.read_excel(file)
            for index, row in data.iterrows():
                Student.objects.create(
                    name=row['姓名'],
                    userid=row['学号'],
                    password=initial_password,
                    class_assigned=new_class
                )
            return redirect('teacher_app:class_teacher')
    return render(request, 'create_class.html', context)


# 班级管理：删除班级
def delete_class(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        if class_id:
            class_to_delete = Class.objects.filter(id=class_id).first()
            if class_to_delete:
                for teacher in class_to_delete.teacher_set.all():
                    teacher.classes_assigned.remove(class_to_delete)
                class_to_delete.delete()
                return JsonResponse({'status': 'success', 'message': '班级删除成功'}, status=200)
        return JsonResponse({'status': 'error', 'message': '班级未找到'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# 班级管理：班级详情
def class_details(request, class_id):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')
    if request.method == 'GET':
        try:
            students = Student.objects.filter(class_assigned=class_id)
            context = {
                'students': students,
                'dropdown_menu1': dropdown_menu1,
                'adminnotifications': adminnotifications
            }
            return render(request, 'class_details.html', context)
        except Class.DoesNotExist:
            return redirect('teacher_app:class_teacher')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('teacher_app:class_teacher')


# 班级管理：删除学生
def delete_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student_to_delete = Student.objects.get(id=student_id)
            student_to_delete.class_assigned = None
            student_to_delete.save()
            student_to_delete.delete()
            return JsonResponse({'status': 'success', 'message': '删除成功'})
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '学生用户不存在'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


# 班级管理：初始化密码
def reset_password(request):
    if request.method == 'POST':
        student = Student.objects.get(id=request.POST.get('student_id'))
        try:
            student.password = 'cumt1909'  # 设置为默认密码
            student.save()
            return JsonResponse({'status': 'success', 'message': '初始化成功，密码改为cumt1909'}, status=200)
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '初始化密码失败'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


# 教师个人中心
def profile_teacher(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')

    context = {
        'dropdown_menu1': dropdown_menu1,
        'teacher': teacher,
        'adminnotifications': adminnotifications
    }
    return render(request, 'profile_teacher.html', context)


# 教师个人中心-编辑
def profile_teacher_edit(request):
    dropdown_menu1 = {'user_id': request.session.get('user_id')}
    teacher = Teacher.objects.get(userid=request.session.get('user_id'))
    adminnotifications = AdminNotification.objects.all().order_by('-date_posted')

    context = {
        'dropdown_menu1': dropdown_menu1,
        'teacher': teacher,
        'adminnotifications': adminnotifications
    }

    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        email = request.POST.get('email')
        teacher.phone_num = phone_num
        teacher.email = email
        teacher.save()
        return redirect('teacher_app:profile_teacher')

    return render(request, 'profile_teacher_edit.html', context)
