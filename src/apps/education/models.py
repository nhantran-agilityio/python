import uuid
from django.db import models

from apps.accounts.models import User


class EducationType(models.TextChoices):
    ACADEMIC = "Academic", "Academic Records"
    PROFESSIONAL = "Professional", "Professional Qualifications"


class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=EducationType.choices, default=EducationType.ACADEMIC,)
