# Generated by Django 5.0.1 on 2024-02-16 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0007_alter_teacher_phone_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='通知内容')),
                ('date_posted', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('recipients', models.ManyToManyField(to='teacher_app.class', verbose_name='接收者')),
            ],
        ),
    ]