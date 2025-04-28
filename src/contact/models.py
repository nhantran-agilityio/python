import uuid
from django.db import models


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_num2 = models.CharField(max_length=20, null=True, blank=True)
    city_of_residence = models.CharField(max_length=100)
    residential_address = models.TextField()
