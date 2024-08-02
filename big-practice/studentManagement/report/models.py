from django.db import models
from core.models import BaseModel


class Report(BaseModel):
    point = models.CharField(max_length=50)
    description = models.CharField(max_length=150)

    student = models.OneToOneField('student.Student', on_delete=models.CASCADE,
                                   related_name='report')
    course = models.OneToOneField('course.Course', on_delete=models.CASCADE,
                                  related_name='report')

    def __str__(self):
        return self.point
