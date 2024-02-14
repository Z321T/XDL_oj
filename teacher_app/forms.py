from django import forms

from .models import Teacher, Class


class TeacherForm(forms.ModelForm):
    userid = forms.CharField(label="教工号", disabled=True)

    class Meta:
        model = Teacher
        fields = ['name', 'userid', 'phone_num', 'email']


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']

