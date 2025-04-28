import uuid
from django.db import models

from accounts.models import User


class Financial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financials')
    bank_name = models.CharField(max_length=100)
    account_no = models.CharField(max_length=30)
    account_name = models.CharField(max_length=100)
