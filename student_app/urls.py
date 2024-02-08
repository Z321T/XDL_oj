# student_app/urls.py
from django.urls import path
from .views import home_student
from .views import practice_student
from .views import test_student
from .views import profile_student
from .views import coding_student
from django.contrib.staticfiles.views import serve

urlpatterns = [
    path('home/', home_student, name='home_student'),
    path('practice/', practice_student, name='practice_student'),
    path('test/', test_student, name='test_student'),
    path('profile/', profile_student, name='profile_student'),
    path('coding/', coding_student, name='coding_student'),
    path('static/<path:path>', serve),
]


