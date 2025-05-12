from django.db import models

from accounts.models import User
from core.models import AbstractBaseModel


class BankAccount(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_account')
    bank_name = models.CharField(max_length=100)
    account_no = models.CharField(max_length=30)
    account_name = models.CharField(max_length=100)
