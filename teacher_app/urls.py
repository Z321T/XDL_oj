from django.urls import path
from .views import home_teacher, test_teacher, profile_teacher, notice_teacher, repository_teacher, class_teacher
from .views import create_class, delete_class, class_details, delete_student, reset_password
from .views import (exercise_list_default, exercise_list,
                    create_exercise, exercise_delete, exercise_edit, exercisequestion_delete)
from .views import (exam_list_default, exam_list,
                    create_exam, exam_delete, exam_edit, examquestion_delete)
from .views import create_notice, delete_notice

from django.contrib.staticfiles.views import serve


app_name = 'teacher_app'


urlpatterns = [
    # 教师使用界面
    # path('home/student/', home_student_views.***, name='')
    path('home/', home_teacher, name='home_teacher'),
    path('test/', test_teacher, name='test_teacher'),
    path('profile/', profile_teacher, name='profile_teacher'),
    # 有关通知的操作
    path('notice/', notice_teacher, name='notice_teacher'),
    path('notice/create/', create_notice, name='create_notice'),
    path('notice/delete/', delete_notice, name='delete_notice'),
    # 有关题库的操作
    path('repository/', repository_teacher, name='repository_teacher'),
    path('repository/exercise_list/', exercise_list_default, name='exercise_list_default'),
    path('repository/exercise_list/<int:exercise_id>/', exercise_list, name='exercise_list'),
    path('repository/exercise_list/create_exercise/<int:exercise_id>/', create_exercise, name='create_exercise'),
    path('repository/delete_exercise/', exercise_delete, name='exercise_delete'),
    path('repository/edit_exercise/<int:exercise_id>/', exercise_edit, name='exercise_edit'),
    path('repository/edit_exercise/exercisequestion_delete/', exercisequestion_delete, name='exercisequestion_delete'),

    path('repository/exam_list/', exam_list_default, name='exam_list_default'),
    path('repository/exam_list/<int:exam_id>/', exam_list, name='exam_list'),
    path('repository/exam_list/create_exam/<int:exam_id>', create_exam, name='create_exam'),
    path('repository/delete_exam/', exam_delete, name='exam_delete'),
    path('repository/edit_exam/<int:exam_id>/', exam_edit, name='exam_edit'),
    path('repository/edit_exam/examquestion_delete/', examquestion_delete, name='examquestion_delete'),
    # 有关班级的操作
    path('class/', class_teacher, name='class_teacher'),
    path('class/create/', create_class, name='create_class'),
    path('class/delete/', delete_class, name='delete_class'),
    path('class/class_details/<int:class_id>', class_details, name='class_details'),
    path('class/class_details/delete_student/', delete_student, name='delete_student'),
    path('class/class_details/reset_password/', reset_password, name='reset_password'),

    path('static/<path:path>', serve),

]