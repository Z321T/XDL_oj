# Generated by Django 5.0.1 on 2024-01-27 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrators',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=6, verbose_name='姓名')),
                ('teacher_id', models.CharField(max_length=10, verbose_name='教工号')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='电子邮件')),
                ('phone_num', models.IntegerField(null=True, verbose_name='电话号码')),
            ],
        ),
    ]
