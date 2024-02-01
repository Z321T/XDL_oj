# Generated by Django 5.0.1 on 2024-01-31 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0002_delete_administrators_delete_teacher'),
        ('teacher_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='teacher_app.teacher', verbose_name='教师'),
        ),
    ]