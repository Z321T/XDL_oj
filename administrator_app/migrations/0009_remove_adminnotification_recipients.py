# Generated by Django 5.0.1 on 2024-02-28 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator_app', '0008_adminnotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminnotification',
            name='recipients',
        ),
    ]
