from django.db import models
import uuid


class JobCategory(models.TextChoices):
    FULL_TIME = "Full Time", "Full Time"
    PART_TIME = "Part Time", "Part Time"


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=100)
    line_management = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    job_category = models.CharField(
        max_length=20,
        choices=JobCategory.choices,
        default=JobCategory.FULL_TIME
    )

    def __str__(self):
        return self.name
