from django.db import models
from core.models import BaseModel


class Course(BaseModel):
    name = models.CharField(max_length=50)
    duration = models.DurationField()
    description = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to='avatars/', null=True, blank=True)
