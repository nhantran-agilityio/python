import uuid
from django.db import models

from apps.accounts.models import User


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    phone_num_1 = models.CharField(max_length=20)
    phone_num_2 = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    city_of_residence = models.CharField(max_length=100)
    residential_address = models.TextField()
