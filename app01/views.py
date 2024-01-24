from django.shortcuts import render, redirect
from app01 import  models

# Create your views here.
def log_in(request):

    return render(request, "log_in.html")