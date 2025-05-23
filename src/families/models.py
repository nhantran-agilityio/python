from django.db import models

from accounts.models import User
from core.models import AbstractBaseModel, BaseModelManager, BaseModelQuerySet


class Family(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_members')
    full_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    objects = BaseModelManager.from_queryset(BaseModelQuerySet)()
