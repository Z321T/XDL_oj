from django.db import models


# Create your models here.
class Teacher(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=6)
    teacher_id = models.CharField(verbose_name="教工号", max_length=10)
    password = models.CharField(verbose_name="密码", max_length=32)
    # department = models.CharField(verbose_name="部门", max_length=16, null=True, blank=True)
    email = models.EmailField(verbose_name="电子邮件", unique=True, null=True, blank=True)
    phone_num = models.IntegerField(verbose_name="电话号码", null=True)

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, null=True, blank=True)


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
