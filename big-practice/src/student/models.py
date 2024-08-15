from django.db import models
from enum import Enum
from django.db.models.functions import Now, ExtractYear, ExtractMonth
from datetime import date
from django.utils import timezone
from datetime import timedelta


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
        twenty_years_ago = today - timedelta(days=20*365.25)  # Approximate 20 years ago
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
        Students_with_age = self.annotate(
            age_years=ExtractYear(Now()) - ExtractYear("birthday"),
            age_months=ExtractMonth(Now()) - ExtractMonth("birthday"),
        )

        # Calculate the average age
        average_age = Students_with_age.aggregate(
            avg_age=models.Avg("age_years") + models.Avg("age_months") / 12
        )["avg_age"]

        return int(average_age)


class Student(models.Model):
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
        today = date.today()
        age = today.year - self.birthday.year - ((today.month, today.day) < (
            self.birthday.month, self.birthday.day))
        return age

    def __str__(self):
        return self.full_name
