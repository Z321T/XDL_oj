from django.urls import path
from student_app import views

app_name = 'student_app'

urlpatterns = [
    # 学生使用界面
    path('home/', views.home, name='home'),
    # path('home/',)
]
