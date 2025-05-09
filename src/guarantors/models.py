from django.db import models

from accounts.models import User
from core.models import AbstractBaseModel


class Guarantor(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guarantors')
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
