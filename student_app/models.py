from django.db import models
from teacher_app.models import Class, ExerciseQuestion, ExamQuestion


# Create your models here.
class Student(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=6)
    userid = models.CharField(verbose_name="学号", max_length=8)
    password = models.CharField(verbose_name="密码", max_length=128)
    email = models.EmailField(verbose_name="邮箱", unique=True, null=True, blank=True)
    last_login = models.DateTimeField(verbose_name='上次登录时间', null=True, blank=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="班级",
                                       null=True, blank=True, related_name='students')


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生", related_name='scores')
    exercise_question = models.ForeignKey(ExerciseQuestion, on_delete=models.CASCADE,
                                          verbose_name="练习题", null=True, blank=True, related_name='scores')
    exam_question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE,
                                      verbose_name="考试题", null=True, blank=True, related_name='scores')
    score = models.DecimalField(verbose_name="得分", max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student.name} - {self.exercise_question or self.exam_question} - {self.score}"

