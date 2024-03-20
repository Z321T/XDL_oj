from django.contrib import admin
from .models import Administrator, AdminNotification, ProgrammingExercise, AdminExam, AdminExamQuestion

# Register your models here
admin.site.register(Administrator)
admin.site.register(AdminNotification)
admin.site.register(ProgrammingExercise)
admin.site.register(AdminExam)
admin.site.register(AdminExamQuestion)
