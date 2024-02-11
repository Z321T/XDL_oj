from django.db import models


# Create your models here.
class Class(models.Model):
    name = models.CharField(verbose_name="班级名称", max_length=255)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=6)
    userid = models.CharField(verbose_name="教工号", max_length=10)
    password = models.CharField(verbose_name="密码", max_length=32)
    # department = models.CharField(verbose_name="部门", max_length=16, null=True, blank=True)
    email = models.EmailField(verbose_name="电子邮件", unique=True, null=True, blank=True)
    phone_num = models.IntegerField(verbose_name="电话号码", null=True)
    last_login = models.DateTimeField(verbose_name='上次登录时间', null=True, blank=True)
    classes_assigned = models.ManyToManyField(Class, verbose_name="所教班级", blank=True)


class Exercise(models.Model):
    title = models.CharField(verbose_name="练习题标题", max_length=255)
    content = models.TextField(verbose_name="练习题内容")
    published_at = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    deadline = models.DateTimeField(verbose_name="截止时间")
    teacher = models.ForeignKey(Teacher, verbose_name="发布教师", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ExerciseQuestion(models.Model):
    exercise = models.ForeignKey(Exercise, verbose_name="练习", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="题目内容")

    def __str__(self):
        return f"{self.exercise.title} - {self.content}"


class ExamQuestion(models.Model):
    content = models.TextField(verbose_name="题目内容")

    def __str__(self):
        return self.content


class Exam(models.Model):
    title = models.CharField(verbose_name="考试标题", max_length=255)
    description = models.TextField(verbose_name="考试描述")
    teacher = models.ForeignKey(Teacher, verbose_name="教师", on_delete=models.CASCADE)
    students = models.ManyToManyField('student_app.Student', verbose_name="参与考试的学生", blank=True)
    questions = models.ManyToManyField(ExamQuestion, verbose_name="考试题目", blank=True)
    published_at = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    deadline = models.DateTimeField(verbose_name="截止时间")

    def __str__(self):
        return self.title


# 写一个新的模型类，用于存储教师的发布的公告，并是与教师关联的学生可以看到公告
class Announcement(models.Model):
    title = models.CharField(verbose_name="公告标题", max_length=255)
    content = models.TextField(verbose_name="公告内容")
    published_at = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    teacher = models.ForeignKey(Teacher, verbose_name="发布教师", on_delete=models.CASCADE)
    students = models.ManyToManyField('student_app.Student', verbose_name="接收公告的学生", blank=True)
    class_to_notify = models.ForeignKey(Class, verbose_name="接收公告的班级", on_delete=models.CASCADE)

    def __str__(self):
        return self.title