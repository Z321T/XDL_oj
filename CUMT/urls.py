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
from django.contrib import admin
from django.urls import path
from app01.views import log_in_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    #统一登录界面
    # path('log/in/', log_in_views.log_in),
    path('log/in/', log_in_views.log_in, name='log_in'),  # 确保这里的 name='log_in' 与模板中的 {% url 'log_in' %} 匹配

    #教师使用界面
    #学生使用界面
    #超级管理员使用界面
]

