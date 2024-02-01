from django.urls import path
from .views import home_teacher
from django.contrib.staticfiles.views import serve


app_name = 'teacher_app'

urlpatterns = [
    # 教师使用界面
    # path('home/student/', home_student_views.***, name='')
   path('home/', home_teacher, name='home_teacher'),
    path('static/<path:path>', serve),

]