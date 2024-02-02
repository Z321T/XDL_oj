from django.urls import path
from .views import home_administrator
from django.contrib.staticfiles.views import serve
from django.contrib import admin

app_name = 'administrator_app'

urlpatterns = [
    # 管理员使用界面
    # path('home/student/', home_student_views.***, name='')
    path('home/', home_administrator, name='home_administrator'),
    path('static/<path:path>', serve),

]
