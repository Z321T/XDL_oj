from django import forms
from django.forms import formset_factory

from .models import Teacher, Class, Exercise, ExerciseQuestion, Exam, ExamQuestion


class TeacherForm(forms.ModelForm):
    userid = forms.CharField(label="教工号", disabled=True)

    class Meta:
        model = Teacher
        fields = ['name', 'userid', 'phone_num', 'email']


class ClassForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Class
        fields = ['name', 'file']


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['title', 'content', 'deadline', 'teacher', 'classes']


class ExerciseQuestionForm(forms.ModelForm):
    class Meta:
        model = ExerciseQuestion
        fields = ['content']


ExerciseQuestionFormset = formset_factory(ExerciseQuestionForm, extra=1)

'''
from django import forms
from django.forms import formset_factory
from .models import Exercise, ExerciseQuestion

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['title', 'content', 'deadline', 'teacher', 'classes']

class ExerciseQuestionForm(forms.ModelForm):
    class Meta:
        model = ExerciseQuestion
        fields = ['content']

ExerciseQuestionFormset = formset_factory(ExerciseQuestionForm, extra=1)
'''