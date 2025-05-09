from django.db import models

from core.models import AbstractBaseModel


class Kin(AbstractBaseModel):
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=50)
    residential_address = models.TextField()

    def __str__(self):
        return self.name
