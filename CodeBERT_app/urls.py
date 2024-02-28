# CodeBERT_app/urls.py
from django.urls import path
from django.contrib.staticfiles.views import serve
from .views import analyze_code, analyze_programming_code

app_name = 'CodeBERT_app'

urlpatterns = [

    path('analyze_code/', analyze_code, name='analyze_code'),
    path('analyze_programming_code/', analyze_programming_code, name='analyze_programming_code'),
    path('static/<path:path>', serve),

]
