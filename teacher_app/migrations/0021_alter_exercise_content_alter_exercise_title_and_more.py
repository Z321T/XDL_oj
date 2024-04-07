# Generated by Django 5.0.1 on 2024-04-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0020_remove_teacher_classes_assigned_class_teacher_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='content',
            field=models.TextField(verbose_name='练习描述'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='title',
            field=models.CharField(max_length=255, verbose_name='练习标题'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='登录时间'),
        ),
    ]
