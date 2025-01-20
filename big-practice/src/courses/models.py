from django.db import models
from django.conf import settings
from django.db.models import Count, Avg
from instructors.models import Instructor


class Course(models.Model):
    name = models.CharField(max_length=50)
    duration = models.DurationField()
    description = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_introductory = models.BooleanField(default=True)
    enrollment_limit = models.PositiveIntegerField(default=30)
    instructors = models.ManyToManyField(Instructor)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def current_enrollments(self):
        return self.enrollment_set.count()

    @property
    def is_full(self):
        return self.current_enrollments >= self.enrollment_limit

    @classmethod
    def average_enrollments(cls):
        return cls.objects.annotate(
            num_enrollments=Count('enrollment')
            ).aggregate(Avg('num_enrollments'))['num_enrollments__avg']

    @classmethod
    def top_courses(cls, limit=5):
        return cls.objects.annotate(
            num_enrollments=Count('enrollment')
            ).order_by('-num_enrollments')[:limit]

class Enrollment(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name="enrollments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="enrollments")

    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
