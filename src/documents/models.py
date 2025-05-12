from django.db import models
from accounts.models import User
from constants.enums import DocumentType
from core.models import AbstractBaseModel


class Document(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='documents')
    document_type = models.CharField(max_length=50,
                                     choices=DocumentType.choices,
                                     default=DocumentType.OFFER_LETTER)
    document_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def file_name(self):
        return self.document_file.name.split('/')[-1]

    @property
    def file_path(self):
        return self.document_file.url

    def __str__(self):
        return f"{self.document_type} - {self.document_file.name}"
