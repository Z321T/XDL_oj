from django.urls import path
from login import views
from student_app.views import home_student
from django.contrib.staticfiles.views import serve

app_name = 'login'

urlpatterns = [
    # 登录界面
    path('', views.log_in, name='log_in'),
    # path('student/home/', home_student, name='home_student'),
    path('static/<path:path>', serve),
]