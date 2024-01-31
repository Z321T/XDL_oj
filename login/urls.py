from django.urls import path
from login import views

app_name = 'login'

urlpatterns = [
    # 登录界面
    path('log/in/', views.log_in, name='log_in')

]