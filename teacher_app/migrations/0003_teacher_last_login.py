# Generated by Django 5.0.1 on 2024-02-04 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0002_examquestion_exam_exercise_exercisequestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='上次登录时间'),
        ),
    ]
