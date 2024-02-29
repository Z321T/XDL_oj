# student_app/urls.py
from django.urls import path
from django.contrib.staticfiles.views import serve

from .views import home_student, practice_student, test_student, profile_student, report_student,analyse_student
from .views import text_list, practice_list, notification_content
from .views import coding_exercise, coding_exam, run_cpp_code


app_name = 'student_app'


urlpatterns = [
    # 学生主页
    path('home/', home_student, name='home_student'),
    path('home/report_student/<int:programmingexercise_id>', report_student, name='report_student'),
    # 学生个人中心
    path('profile/', profile_student, name='profile_student'),
    # 通知相关
    path('notification_content/', notification_content, name='notification_content'),
    # 练习相关
    path('practice/', practice_student, name='practice_student'),
    path('practice/practice_list/<int:exercise_id>/', practice_list, name='practice_list'),
    path('coding_exercise/<int:exercisequestion_id>/', coding_exercise, name='coding_exercise'),
    # 考试相关
    path('test/', test_student, name='test_student'),
    path('test/text_list/<int:exam_id>/', text_list, name='text_list'),
    path('coding_exam/<int:examquestion_id>/', coding_exam, name='coding_exam'),
    # 学情分析相关
    path('analyse/', analyse_student, name='analyse_student'),


    # 编码运行相关
    path('run-cpp/', run_cpp_code, name='run-cpp'),

    path('static/<path:path>', serve),
]


