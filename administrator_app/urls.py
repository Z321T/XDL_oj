from django.urls import path
from django.contrib.staticfiles.views import serve
from django.contrib import admin

from .views import home_administrator
from .views import class_administrator
from .views import notice_administrator
from .views import profile_administrator
from .views import repository_administrator
from .views import test_administrator
from .views import plagiarism_administrator
from .views import information_administrator
from .views import problems_administrator


app_name = 'administrator_app'

urlpatterns = [
    # 管理员使用界面
    # path('home/student/', home_student_views.***, name='')
    path('home/', home_administrator, name='home_administrator'),
    path('class/', class_administrator, name='class_administrator'),
    path('notice/', notice_administrator, name='notice_administrator'),
    path('profile/', profile_administrator, name='profile_administrator'),
    path('repository/', repository_administrator, name='repository_administrator'),
    path('test/', test_administrator, name='test_administrator'),
    path('plagiarism/', plagiarism_administrator, name='plagiarism_administrator'),
    path('information/', information_administrator, name='information_administrator'),
    path('problems/', problems_administrator, name='problems_administrator'),

    path('static/<path:path>', serve),

]
