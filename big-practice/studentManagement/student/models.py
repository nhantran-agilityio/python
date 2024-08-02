from django.db import models
from core.models import BaseModel, ExtendedEnum
from django.db.models.functions import Now, ExtractYear, ExtractMonth


class Gender(ExtendedEnum):
    """
    Enum class representing different gender for student
    """
    MALE = "male"
    FE_MALE = "fe-male"


class StudentManager(models.Manager):
    def students_over_point_5(self):
        """
        Get Students point large than 5.

        Returns:
            QuerySet: QuerySet containing Students point larger than 5
        """

        return self.filter(student__report__point__gt=5).distinct()

    def active_Students(self):
        """
        Get active Student.

        Returns:
            QuerySet: QuerySet containing active Students.
        """
        return self.filter(is_active=True)

    def Student_avg_age(self):
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


class Student(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    gender: str = models.CharField(choices=Gender.choices(), max_length=50)
    birthday = models.DateField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    courses = models.ManyToManyField(
        'courses.Course', on_delete=models.CASCADE, related_name="student")
    report = models.OneToOneField('Report', on_delete=models.CASCADE,
                                  related_name='student')
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

    def __str__(self):
        return self.full_name
