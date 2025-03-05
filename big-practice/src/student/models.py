from django.db import models
from enum import Enum
from django.db.models.functions import ExtractYear, ExtractMonth
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class Gender(Enum):
    """
    Enum class representing different gender for student
    """
    MALE = "male"
    FE_MALE = "fe-male"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class StudentManager(models.Manager):
    def student_over_20(self):
        today = timezone.now().date()
        # Approximate 20 years ago
        twenty_years_ago = today - timedelta(days=20*365.25)
        return self.filter(birthday__lte=twenty_years_ago)

    def active_Students(self):
        """
        Get active Student.

        Returns:
            QuerySet: QuerySet containing active Students.
        """
        return self.filter(is_active=True)

    def student_avg_age(self):
        """

        Get average age of Student.

        Returns:
            int: Average age of Student
        """
        # Calc Student age
        students_with_age = self.annotate(
            age_years=ExtractYear(timezone.now()) - ExtractYear("birthday"),
            age_months=ExtractMonth(timezone.now()) - ExtractMonth("birthday"),
        )

        # Calculate the average age
        average_age = students_with_age.aggregate(
            avg_age=models.Avg("age_years") + models.Avg("age_months") / 12
        )["avg_age"]

        return int(average_age)


class Student(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )  # Allow NULL
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    gender: str = models.CharField(choices=Gender.choices(), max_length=50)
    birthday = models.DateField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    courses = models.ManyToManyField('courses.Course', related_name='student',
                                     blank=True)
    objects = StudentManager()

    # Custom property
    @property
    def full_name(self) -> str:
        """
        Return the full_name by combine value of first_name and last_name

        Returns:
            str: Full student name
        """
        return f"{self.first_name} {self.last_name}"

    def get_age(self):
        today = timezone.now().date()
        age = today.year - self.birthday.year
        age -= (today.month, today.day) < (
            self.birthday.month, self.birthday.day)
        return age

    def __str__(self):
        return self.full_name

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
            models.Index(fields=['birthday']),
        ]
