from django.shortcuts import render

# Create your views here.
def home_administrator(request):
    return render(request, 'home_administrator.html')
