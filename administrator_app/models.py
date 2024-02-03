# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
#
# # 超级管理员用户
# class Administrator(AbstractUser):
#     name = models.CharField(verbose_name="姓名", max_length=6)
#     admin_id = models.CharField(verbose_name="教工号", max_length=10, unique=True)
#     email = models.EmailField(verbose_name="电子邮件", unique=True, null=True, blank=True)
#     phone_num = models.IntegerField(verbose_name="电话号码", null=True)
#
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='admin_groups',  # 为避免冲突，给定一个自定义的 related_name
#         blank=True,
#         verbose_name='Groups',
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#     )
#
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='admin_user_permissions',  # 同样，给定一个自定义的 related_name
#         blank=True,
#         verbose_name='User permissions',
#         help_text='Specific permissions for this user.',
#         related_query_name='admin_user',
#     )


from django.db import models


# Create your models here.
class Administrator(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=6)
    admin_id = models.CharField(verbose_name="教工号", max_length=10)
    password = models.CharField(verbose_name="密码", max_length=32)
    # department = models.CharField(verbose_name="部门", max_length=16, null=True, blank=True)
    email = models.EmailField(verbose_name="电子邮件", unique=True, null=True, blank=True)
    phone_num = models.IntegerField(verbose_name="电话号码", null=True)
    last_login = models.DateTimeField(verbose_name='上次登录时间', null=True, blank=True)

