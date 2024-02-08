from django.contrib import admin
from .models import Teacher, Exercise, ExerciseQuestion, ExamQuestion, Exam

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Exercise)
admin.site.register(ExerciseQuestion)
admin.site.register(ExamQuestion)
admin.site.register(Exam)

