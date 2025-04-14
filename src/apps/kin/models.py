import uuid
from django.db import models


class Kin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=50)
    residential_address = models.TextField()
