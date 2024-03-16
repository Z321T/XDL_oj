from django.db import models


# Create your models here.
class Administrator(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=6)
    userid = models.CharField(verbose_name="教工号", max_length=10)
    password = models.CharField(verbose_name="密码", max_length=128)
    email = models.EmailField(verbose_name="电子邮件", unique=True, null=True, blank=True)
    phone_num = models.CharField(verbose_name="电话号码", max_length=12, null=True)
    last_login = models.DateTimeField(verbose_name='上次登录时间', null=True, blank=True)


class AdminNotification(models.Model):
    title = models.CharField(verbose_name="通知标题", max_length=255, null=True, blank=True)
    content = models.TextField(verbose_name="通知内容")
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")


class ProgrammingExercise(models.Model):
    title = models.CharField(verbose_name="题目标题", max_length=255)
    description = models.TextField(verbose_name="题目描述")
    posted_by = models.ForeignKey(Administrator, verbose_name="发布教师", on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    deadline = models.DateTimeField(verbose_name="截止时间")

    def __str__(self):
        return self.title
