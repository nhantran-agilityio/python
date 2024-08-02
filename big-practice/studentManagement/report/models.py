from django.db import models
from core.models import BaseModel


class Report(BaseModel):
    grades = models.CharField(max_length=50)
    description = models.CharField(max_length=150)

