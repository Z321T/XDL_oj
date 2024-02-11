# Generated by Django 5.0.1 on 2024-02-11 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0005_class_remove_teacher_gender_announcement_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='description',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='announcement',
            name='students',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='questions',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='students',
        ),
        migrations.AddField(
            model_name='exam',
            name='classes',
            field=models.ManyToManyField(blank=True, to='teacher_app.class', verbose_name='参与考试的班级'),
        ),
        migrations.AddField(
            model_name='examquestion',
            name='exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='teacher_app.exam', verbose_name='考试'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='classes',
            field=models.ManyToManyField(blank=True, to='teacher_app.class', verbose_name='参与练习的班级'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='content',
            field=models.TextField(verbose_name='练习题描述'),
        ),
        migrations.AlterField(
            model_name='exercisequestion',
            name='exercise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='teacher_app.exercise', verbose_name='练习'),
        ),
    ]
