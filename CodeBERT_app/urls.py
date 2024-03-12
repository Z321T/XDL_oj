# CodeBERT_app/urls.py
from django.urls import path
from django.contrib.staticfiles.views import serve
# from .views import (analyze_code, analyze_programming_code, analyze_programming_report,
#                     compute_cosine_similarity, score_report,)

app_name = 'CodeBERT_app'

urlpatterns = [

    # path('analyze_code/', analyze_code, name='analyze_code'),
    # path('analyze_programming_code/', analyze_programming_code, name='analyze_programming_code'),
    # path('analyze_programming_report/', analyze_programming_report, name='analyze_programming_report'),
    # path('compute_cosine_similarity/', compute_cosine_similarity, name='compute_cosine_similarity'),
    # path('score_report/', score_report, name='score_report'),
    path('static/<path:path>', serve),

]
