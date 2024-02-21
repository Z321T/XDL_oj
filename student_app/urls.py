# student_app/urls.py
from django.urls import path
from django.contrib.staticfiles.views import serve

from .views import home_student, practice_student, test_student, profile_student, coding_student
from .views import text_list, practice_list, notification_content
from . import views


app_name = 'student_app'


urlpatterns = [
    path('home/', home_student, name='home_student'),
    # 练习相关
    path('practice/', practice_student, name='practice_student'),
    path('practice/practice_list/<int:exercise_id>', practice_list, name='practice_list'),
    # 考试相关
    path('test/', test_student, name='test_student'),
    path('test/text_list/<int:exam_id>', text_list, name='text_list'),
    # 练习相关
    path('profile/', profile_student, name='profile_student'),
    path('practice/practice_list/<int:exercise_id>', practice_list, name='practice_list'),

    path('profile/', profile_student, name='profile_student'),
    path('notification_content/', notification_content, name='notification_content'),
    path('coding/', coding_student, name='coding_student'),
    path('run-cpp/', views.run_cpp_code, name='run-cpp'),


    path('static/<path:path>', serve),
]


