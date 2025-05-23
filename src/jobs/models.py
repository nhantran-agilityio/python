from django.db import models
from constants.enums import JobCategory
from core.models import AbstractBaseModel, BaseModelManager, BaseModelQuerySet


class Job(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=100)
    responsibilities = models.JSONField(blank=True, null=True)
    job_category = models.CharField(
        max_length=20,
        choices=JobCategory.choices,
        default=JobCategory.FULL_TIME
    )
    line_management = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_jobs",
    )
    objects = BaseModelManager.from_queryset(BaseModelQuerySet)()

    def get_line_management(self):
        if self.line_management:
            return f"{self.line_management.first_name} {self.line_management.last_name}"
        return 'No Manager'

    def __str__(self):
        return self.name
