from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=6)
    student_id = models.CharField(verbose_name="学号", max_length=8)
    password = models.CharField(verbose_name="密码", max_length=32)
    class_num = models.CharField(verbose_name="班级", max_length=32, blank=True)
    email = models.EmailField(verbose_name="电子邮件", unique=True, null=True, blank=True)

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, null=True, blank=True)

    # 添加外键字段，表示每个学生属于一个教师
    teacher = models.ForeignKey('teacher_app.Teacher', verbose_name="教师", on_delete=models.SET_NULL, null=True, blank=True)






