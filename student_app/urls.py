# student_app/urls.py
from django.urls import path
from django.contrib.staticfiles.views import serve

from .views import home_student
from .views import practice_student
from .views import test_student
from .views import profile_student
from .views import coding_student
# from .views import student_info

urlpatterns = [
    path('home/', home_student, name='home_student'),
    path('practice/', practice_student, name='practice_student'),
    path('test/', test_student, name='test_student'),
    path('profile/', profile_student, name='profile_student'),
    path('coding/', coding_student, name='coding_student'),

    # path('student_info/', student_info, name='student_info'),





    path('static/<path:path>', serve),
]


