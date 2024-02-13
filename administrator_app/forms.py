from django import forms
from .models import Administrator


class AdministratorForm(forms.ModelForm):
    userid = forms.CharField(label="教工号", disabled=True)

    class Meta:
        model = Administrator
        fields = ['name', 'userid', 'phone_num', 'email', ]