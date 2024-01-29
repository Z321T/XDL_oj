from django.db import models

# Create your models here.
class Administrator(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=6)
    teacher_id = models.CharField(verbose_name="教工号", max_length=10)
    password = models.CharField(verbose_name="密码", max_length=32)
    # department = models.CharField(verbose_name="部门", max_length=16, null=True, blank=True)
    email = models.EmailField(verbose_name="电子邮件", unique=True, null=True, blank=True)
    phone_num = models.IntegerField(verbose_name="电话号码", null=True)

