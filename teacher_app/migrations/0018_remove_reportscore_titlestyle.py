# Generated by Django 5.0.1 on 2024-03-13 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_app', '0017_reportscore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportscore',
            name='titlestyle',
        ),
    ]
