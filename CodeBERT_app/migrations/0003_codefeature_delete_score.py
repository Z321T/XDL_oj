# Generated by Django 5.0.1 on 2024-02-21 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CodeBERT_app', '0002_initial'),
        ('student_app', '0018_score'),
        ('teacher_app', '0016_examquestion_answer_exercisequestion_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.TextField(verbose_name='特征值')),
                ('exam_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='code_features', to='teacher_app.examquestion', verbose_name='考试题')),
                ('exercise_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='code_features', to='teacher_app.exercisequestion', verbose_name='练习题')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='code_features', to='student_app.student', verbose_name='学生')),
            ],
        ),
        migrations.DeleteModel(
            name='Score',
        ),
    ]
