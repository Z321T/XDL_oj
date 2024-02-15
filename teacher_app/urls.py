from django.urls import path
from .views import home_teacher, test_teacher, profile_teacher, notice_teacher, repository_teacher, class_teacher
from .views import create_class

from django.contrib.staticfiles.views import serve


app_name = 'teacher_app'

urlpatterns = [
    # 教师使用界面
    # path('home/student/', home_student_views.***, name='')
    path('home/', home_teacher, name='home_teacher'),
    path('test/', test_teacher, name='test_teacher'),
    path('profile/', profile_teacher, name='profile_teacher'),
    path('notice/', notice_teacher, name='notice_teacher'),
    path('repository/', repository_teacher, name='repository_teacher'),
    path('class/', class_teacher, name='class_teacher'),
    path('class/create/', create_class, name='create_class'),


    path('static/<path:path>', serve),

]