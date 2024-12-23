# Generated by Django 5.0.1 on 2024-03-23 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0019_alter_teacher_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='classes_assigned',
        ),
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teacher_app.teacher', verbose_name='教师'),
        ),
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(max_length=30, verbose_name='班级名称'),
        ),
    ]
