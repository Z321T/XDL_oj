from django.urls import path
from .views import home_teacher
from .views import test_teacher
from .views import profile_teacher
from .views import notice_teacher
from .views import repository_teacher

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

    path('static/<path:path>', serve),

]