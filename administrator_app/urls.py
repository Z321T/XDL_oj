from django.urls import path
from administrator_app import views
from .views import home_administrator
from django.contrib.staticfiles.views import serve

app_name = 'administrator_app'

urlpatterns = [
    # 管理员使用界面
    # path('home/student/', home_student_views.***, name='')
    path('home/', home_administrator, name='home_administrator'),
    path('static/<path:path>', serve),

]
