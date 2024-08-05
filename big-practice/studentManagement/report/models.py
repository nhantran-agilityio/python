from django.db import models


class Report(models.Model):
    point = models.PositiveIntegerField()
    description = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE,
                                null=True, related_name='report')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE,
                               null=True, related_name='report')

    class Meta:
        # Ensures that each student-course pair is unique
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.full_name} - {self.course.name} - {self.point}"
