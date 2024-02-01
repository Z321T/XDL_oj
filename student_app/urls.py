# student_app/urls.py
from django.urls import path
from .views import home_student
from django.contrib.staticfiles.views import serve

urlpatterns = [
    path('home/', home_student, name='home_student'),
    path('static/<path:path>', serve),
]


