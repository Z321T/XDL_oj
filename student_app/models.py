from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=6)
    userid = models.CharField(verbose_name="学号", max_length=8)
    password = models.CharField(verbose_name="密码", max_length=128)
    email = models.EmailField(verbose_name="电子邮箱", unique=True, null=True, blank=True)
    last_login = models.DateTimeField(verbose_name='上次登录时间', null=True, blank=True)


