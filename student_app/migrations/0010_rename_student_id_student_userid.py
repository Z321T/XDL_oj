# Generated by Django 5.0.1 on 2024-02-09 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0009_alter_student_email_alter_student_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='student_id',
            new_name='userid',
        ),
    ]
