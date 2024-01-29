"""
URL configuration for CUMT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
import student_app.views
import teacher_app.views
import administrator_app.views

urlpatterns = [

    #统一登录界面
    path('log/in/', student_app.views.log_in, name='log_in'),  # 这里的 name='log_in'与模板中的 {% url 'log_in' %} 匹配

    #学生使用界面
    path('student/', include('student_app.urls')),
    # path('home/student/', home_student_views.***, name='')

    # #教师使用界面
    # path('teacher/', include('teacher_app.urls')),

    # #超级管理员使用界面
    # path('administrator/', include('administrator_app'))

]

