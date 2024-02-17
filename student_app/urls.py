# student_app/urls.py
from django.urls import path
from django.contrib.staticfiles.views import serve

from .views import home_student, practice_student, test_student, profile_student, coding_student


app_name = 'student_app'

urlpatterns = [
    path('home/', home_student, name='home_student'),
    path('practice/', practice_student, name='practice_student'),
    path('test/', test_student, name='test_student'),
    path('profile/', profile_student, name='profile_student'),
    path('coding/', coding_student, name='coding_student'),


    path('static/<path:path>', serve),
]


