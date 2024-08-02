from django.db import models
from core.models import BaseModel, ExtendedEnum


class Gender(ExtendedEnum):
    """
    Enum class representing different gender for student
    """
    MALE = "male"
    FE_MALE = "fe-male"


class Student(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    gender: str = models.CharField(choices=Gender.choices(), max_length=50)
    birthday = models.DateField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    courses = models.ManyToManyField(
        'courses.Course', on_delete=models.CASCADE, related_name="student")

    def __str__(self):
        return self.name

    # Custom property
    @property
    def full_name(self) -> str:
        """
        Return the full_name by combine value of first_name and last_name

        Returns:
            str: Full student name
        """
        return f"{self.first_name} {self.last_name}"

