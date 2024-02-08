import json
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages
from student_app.models import Student
from teacher_app.models import Teacher
from administrator_app.models import Administrator
from django.http import HttpResponse, JsonResponse
from .forms import StudentForm


# Create your views here.
def home_student(request):
    return render(request, 'home_student.html')


def practice_student(request):
    return render(request, 'practice_student.html')


def test_student(request):
    return render(request, 'test_student.html')

def coding_student(request):
    return render(request, 'coding_student.html')



def profile_student(request):
    if request.method == 'GET':
        user_name = request.session.get('user_id')  # 获取用户名
        if user_name is not None:
            try:
                student = Student.objects.get(name=user_name)
                return render(request, 'profile_student.html', {'student': student})
            except ObjectDoesNotExist:
                return HttpResponse('User not found', status=404)
        else:
            return HttpResponse('User not found', status=404)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_name = request.session.get('user_id')  # 获取用户名
            student = Student.objects.get(name=user_name)
            student.name = data['name']
            student.student_id = data['student_id']
            student.class_num = data['class']
            student.email = data['email']
            student.save()
            return JsonResponse({'status': 'success'})
        except (json.JSONDecodeError, KeyError, ObjectDoesNotExist) as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    else:
        return HttpResponse('Method not allowed', status=405)
# def profile_student(request):
#     return render(request, 'profile_student.html')


# def profile_student(request):
#     user_name = request.session.get('user_id')  # 获取用户名
#     student = Student.objects.get(name=user_name)
#     if request.method == 'POST':
#         form = StudentForm(request.POST, instance=student)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully')
#             return redirect('profile_student')
#     else:
#         form = StudentForm(instance=student)
#     return render(request, 'profile_student.html', {'form': form})

# def student_info(request):
#     if request.method == 'GET':
#         user_name = request.session.get('user_id')  # 获取用户名
#         if user_name is not None:
#             student = Student.objects.get(name=user_name)
#             return JsonResponse({'name': student.name, 'student_id': student.student_id, 'class': student.class_num, 'email': student.email})
#
#     elif request.method == 'POST':
#         data = json.loads(request.body)
#         user_name = request.session.get('user_id')  # 获取用户名
#         student = Student.objects.get(name=user_name)
#         student.name = data['name']
#         student.student_id = data['student_id']
#         student.class_num = data['class']
#         student.email = data['email']
#         student.save()
#         return JsonResponse({'status': 'success'}, status=200)
