from django.db import models

from administrator_app.models import ProgrammingExercise
from student_app.models import Student
from teacher_app.models import ExerciseQuestion, ExamQuestion


# Create your models here.
class CodeFeature(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, verbose_name="学生",
                                related_name='code_features', null=True)
    exercise_question = models.ForeignKey(ExerciseQuestion, on_delete=models.CASCADE,
                                          verbose_name="练习题", related_name='code_features', null=True, blank=True)
    exam_question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE,
                                      verbose_name="考试题", related_name='code_features', null=True, blank=True)
    feature = models.TextField(verbose_name="特征值")

    def __str__(self):
        return (f"{self.student.name if self.student else '无关联学生'} - "
                f"{self.exercise_question or self.exam_question} - {self.feature}")


class ProgrammingCodeFeature(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, verbose_name="学生",
                                related_name='programming_code_features', null=True)
    programming_question = models.ForeignKey(ProgrammingExercise, on_delete=models.CASCADE, verbose_name="练习题",
                                             related_name='programming_code_features', null=True, blank=True)
    feature = models.TextField(verbose_name="特征值")
    cosine_similarity = models.FloatField(verbose_name="余弦相似度", null=True, blank=True)

    def __str__(self):
        return (f"{self.student.name if self.student else '无关联学生'} - "
                f"{self.programming_question} - {self.feature}")


