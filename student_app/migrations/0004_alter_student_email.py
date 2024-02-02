# Generated by Django 5.0.1 on 2024-02-02 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0003_student_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='电子邮件'),
        ),
    ]