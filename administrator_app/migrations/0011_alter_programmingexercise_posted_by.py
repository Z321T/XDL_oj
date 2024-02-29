# Generated by Django 5.0.1 on 2024-02-29 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator_app', '0010_programmingexercise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmingexercise',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator_app.administrator', verbose_name='发布教师'),
        ),
    ]
