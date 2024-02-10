from django.shortcuts import render


# Create your views here.
def home_teacher(request):
    dropdown_menu1 = {
        'user_id': request.session.get('user_id'),
    }
    return render(request, 'home_teacher.html', {'dropdown_menu1': dropdown_menu1})