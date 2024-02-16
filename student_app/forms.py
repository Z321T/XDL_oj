from django import forms
from .models import Student
from teacher_app.models import Class


class StudentForm(forms.ModelForm):
    userid = forms.CharField(label="学号", disabled=True)
    class_assigned = forms.ModelChoiceField(queryset=Class.objects.all(), label="班级", disabled=True)

    class Meta:
        model = Student
        fields = ['name', 'userid', 'class_assigned', 'email', ]