# Generated by Django 5.0.1 on 2024-02-03 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator_app', '0003_alter_administrator_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrator',
            options={},
        ),
        migrations.AlterModelManagers(
            name='administrator',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='administrator',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='administrator',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='administrator',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='administrator',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='administrator',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='administrator',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='administrator',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='administrator',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='administrator',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='administrator',
            name='username',
        ),
        migrations.AlterField(
            model_name='administrator',
            name='admin_id',
            field=models.CharField(max_length=10, verbose_name='教工号'),
        ),
        migrations.AlterField(
            model_name='administrator',
            name='password',
            field=models.CharField(max_length=32, verbose_name='密码'),
        ),
    ]
