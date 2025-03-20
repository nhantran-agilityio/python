from django.db import models
import uuid
from apps.job.models import Job


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='documents')
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    upload_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.file_name
