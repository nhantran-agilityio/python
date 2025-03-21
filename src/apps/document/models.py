from django.db import models
import uuid
from apps.job.models import Job


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('offer_letter', 'Offer Letter'),
        ('birth_certificate', 'Birth Certificate'),
        ('guarantor_form', 'Guarantor’s Form'),
        ('degree_certificate', 'Degree Certificate'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def file_name(self):
        return self.document_file.name.split('/')[-1]

    @property
    def file_path(self):
        return self.document_file.url

    def __str__(self):
        return self.file_name
