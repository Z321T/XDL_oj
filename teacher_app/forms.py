from django import forms
from .models import Teacher


class TeacherForm(forms.ModelForm):
    userid = forms.CharField(label="教工号", disabled=True)

    class Meta:
        model = Teacher
        fields = ['name', 'userid', 'phone_num', 'email', ]