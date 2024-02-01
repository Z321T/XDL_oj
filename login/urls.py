from django.urls import path
from login import views
from django.contrib.staticfiles.views import serve

app_name = 'login'

urlpatterns = [
    # 登录界面
    path('', views.log_in, name='log_in'),
    path('static/<path:path>', serve),
]