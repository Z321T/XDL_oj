from django.db import models


# Create your models here.
class Score(models.Model):
    student = models.ForeignKey('student_app.Student', on_delete=models.CASCADE, verbose_name="学生")
    exam = models.ForeignKey('teacher_app.Exam', on_delete=models.CASCADE, null=True, blank=True, verbose_name="考试")
    exercise = models.ForeignKey('teacher_app.Exercise', on_delete=models.CASCADE, null=True, blank=True, verbose_name="练习")
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="得分")

    def __str__(self):
        return f"{self.student.name} - {self.exam.title if self.exam else self.exercise.title} - {self.score}"

