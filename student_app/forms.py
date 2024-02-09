from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    userid = forms.CharField(label="学号", disabled=True)

    class Meta:
        model = Student
        fields = ['name', 'userid', 'class_num', 'email', ]