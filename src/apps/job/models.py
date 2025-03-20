from django.db import models
import uuid
from apps.accounts.models import User


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_jobs')
    name = models.CharField(max_length=100)
    description = models.TextField()
    role = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    line_management = models.BigIntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
