from django.urls import path
from django.contrib.staticfiles.views import serve

from .views import home_administrator, programmingexercise_details_data
from .views import notice_administrator, create_notice, delete_notice, notification_content
from .views import profile_administrator, profile_administrator_edit
from .views import repository_administrator, programmingexercise_delete, programmingexercise_create
from .views import information_administrator, add_teacher, delete_teacher, reset_password
from .views import problems_administrator, report_administrator
from .views import (exam_administrator, adminexam_list_default, adminexam_list,
                    create_adminexam, adminexam_edit, adminexam_delete, adminexamquestion_delete)


app_name = 'administrator_app'

urlpatterns = [
    # 管理员使用界面
    path('home/', home_administrator, name='home_administrator'),
    path('home/programmingexercise_details_data/', programmingexercise_details_data, name='programmingexercise_details_data'),
    # 有关程序设计题库的操作
    path('repository/', repository_administrator, name='repository_administrator'),
    path('repository/programmingexercise_delete/', programmingexercise_delete, name='programmingexercise_delete'),
    path('repository/programmingexercise_create/', programmingexercise_create, name='programmingexercise_create'),
    # 题库查重管理
    path('problems/', problems_administrator, name='problems_administrator'),
    path('problems/report_administrator/', report_administrator, name='report_administrator'),
    # 有关考试的操作
    path('exam/', exam_administrator, name='exam_administrator'),
    path('exam/exam_list/', adminexam_list_default, name='adminexam_list_default'),
    path('exam/exam_list/<int:exam_id>/', adminexam_list, name='adminexam_list'),
    path('exam/exam_list/create_exam/<int:exam_id>/', create_adminexam, name='create_adminexam'),
    path('exam/delete_exam/', adminexam_delete, name='adminexam_delete'),
    path('exam/edit_exam/<int:exam_id>/', adminexam_edit, name='adminexam_edit'),
    path('exam/edit_exam/adminexamquestion_delete/', adminexamquestion_delete, name='adminexamquestion_delete'),
    # 有关通知的操作
    path('notice/', notice_administrator, name='notice_administrator'),
    path('notice/create/', create_notice, name='create_notice'),
    path('notice/delete/', delete_notice, name='delete_notice'),
    path('notice/notification_content/', notification_content, name='notification_content'),
    # 教师管理
    path('information/', information_administrator, name='information_administrator'),
    path('information/add_teacher/', add_teacher, name='add_teacher'),
    path('information/delete_teacher/', delete_teacher, name='delete_teacher'),
    path('information/reset_password/', reset_password, name='reset_password'),
    # 个人中心
    path('profile/', profile_administrator, name='profile_administrator'),
    path('profile/edit/', profile_administrator_edit, name='profile_administrator_edit'),

    path('static/<path:path>', serve),

]
