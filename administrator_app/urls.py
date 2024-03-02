from django.urls import path
from django.contrib.staticfiles.views import serve

from .views import home_administrator
from .views import notice_administrator, create_notice, delete_notice, notification_content
from .views import profile_administrator, profile_administrator_edit
from .views import repository_administrator, programmingexercise_delete, programmingexercise_create
from .views import information_administrator, add_teacher, delete_teacher
from .views import problems_administrator


app_name = 'administrator_app'

urlpatterns = [
    # 管理员使用界面
    path('home/', home_administrator, name='home_administrator'),
    # 有关通知的操作
    path('notice/', notice_administrator, name='notice_administrator'),
    path('notice/create/', create_notice, name='create_notice'),
    path('notice/delete/', delete_notice, name='delete_notice'),
    path('notice/notification_content/', notification_content, name='notification_content'),
    # 有关程序设计题库的操作
    path('repository/', repository_administrator, name='repository_administrator'),
    path('repository/programmingexercise_delete/', programmingexercise_delete, name='programmingexercise_delete'),
    path('repository/programmingexercise_create/', programmingexercise_create, name='programmingexercise_create'),
    # 个人中心
    path('profile/', profile_administrator, name='profile_administrator'),
    path('profile/edit/', profile_administrator_edit, name='profile_administrator_edit'),
    # 题库查重管理
    path('problems/', problems_administrator, name='problems_administrator'),
    # 教师管理
    path('information/', information_administrator, name='information_administrator'),
    path('information/add_teacher/', add_teacher, name='add_teacher'),
    path('information/delete_teacher/', delete_teacher, name='delete_teacher'),


    path('static/<path:path>', serve),

]
