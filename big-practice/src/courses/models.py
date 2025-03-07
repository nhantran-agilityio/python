from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db import models
from django.db.models import Count, Avg, QuerySet
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class Course(models.Model):
    name = models.CharField(max_length=50)
    duration = models.DurationField(null=True)
    description = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_introductory = models.BooleanField(default=True)
    enrollment_limit = models.PositiveIntegerField(default=2)
    instructors = models.ManyToManyField('instructors.Instructor')
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    enrollments = models.ManyToManyField(
        'student.Student',
        through='Enrollment',
        related_name='enrolled_courses'
    )

    def __str__(self):
        return self.name

    @property
    def current_enrollments(self):
        return self.enrollments.count()

    @property
    def is_full(self):
        return self.current_enrollments >= self.enrollment_limit

    @classmethod
    def average_enrollments(cls):
        return cls.objects.annotate(
            num_enrollments=Count('course_enrollments')
        ).aggregate(Avg('num_enrollments'))['num_enrollments__avg']

    @classmethod
    def top_courses(cls, limit: int = 5) -> QuerySet:
        """Get the top courses by enrollment count, up to a limit."""
        cached_top_courses = cache.get('top_courses')

        if cached_top_courses is not None:
            return cached_top_courses

        top_courses = (
            cls.objects.annotate(num_enrollments=Count('course_enrollments'))
            .order_by('-num_enrollments')[:limit]
        )
        cache.set('top_courses', top_courses, timeout=CACHE_TTL)
        logger.debug(f"Returning top courses: {top_courses}")
        return top_courses


class Enrollment(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_enrollments"
    )
    student = models.ForeignKey(
        'student.Student', on_delete=models.CASCADE,
        related_name="student_enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} enrolled in {self.course.name}"

    class Meta:
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['student']),
            models.Index(fields=['enrolled_at']),
        ]
