# Generated by Django 5.0.1 on 2024-01-27 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Administrator',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
