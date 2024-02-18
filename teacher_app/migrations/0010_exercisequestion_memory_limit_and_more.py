# Generated by Django 5.0.1 on 2024-02-18 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0009_alter_notification_recipients_delete_announcement'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercisequestion',
            name='memory_limit',
            field=models.IntegerField(default=0, verbose_name='内存限制'),
        ),
        migrations.AddField(
            model_name='exercisequestion',
            name='time_limit',
            field=models.IntegerField(default=0, verbose_name='时间限制'),
        ),
        migrations.AddField(
            model_name='exercisequestion',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='题目标题'),
        ),
    ]
