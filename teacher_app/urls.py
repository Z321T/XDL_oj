from django.urls import path
from .views import home_teacher, test_teacher, profile_teacher, notice_teacher, repository_teacher, class_teacher
from .views import create_class, delete_class, get_students
from .views import create_exercise, create_exam

from django.contrib.staticfiles.views import serve


app_name = 'teacher_app'

urlpatterns = [
    # 教师使用界面
    # path('home/student/', home_student_views.***, name='')
    path('home/', home_teacher, name='home_teacher'),
    path('test/', test_teacher, name='test_teacher'),
    path('profile/', profile_teacher, name='profile_teacher'),
    path('notice/', notice_teacher, name='notice_teacher'),
    # 有关题库的操作
    path('repository/', repository_teacher, name='repository_teacher'),
    path('repository/create_exercise/', create_exercise, name='create_exercise'),
    path('repository/create_exam/', create_exam, name='create_exam'),
    # 有关班级的操作
    path('class/', class_teacher, name='class_teacher'),
    path('class/create/', create_class, name='create_class'),
    path('class/delete/', delete_class, name='delete_class'),
    path('class/get_students/', get_students, name='get_students'),

    path('static/<path:path>', serve),

]