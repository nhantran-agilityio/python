from django.db import models
from django.contrib.auth.models import AbstractUser
from constants.enums import RoleChoices
from core.models import AbstractBaseModel
from jobs.models import Job
from kins.models import Kin


class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    CANDIDATE = "candidate", "Candidate"
    EMPLOYEE = "employee", "Employee"


class User(AbstractBaseModel, AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    phone_num2 = models.CharField(max_length=20, null=True, blank=True)
    city_of_residence = models.CharField(max_length=100, null=True, blank=True)
    residential_address = models.TextField(max_length=100, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.EMPLOYEE.value
    )
    is_receive_newsletters = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )
    job = models.ForeignKey(
        Job,
        related_name='users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    kin = models.ForeignKey(
        Kin,
        related_name='users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        """
        Checks if the user is an admin.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return self.role == Role.ADMIN

    def __str__(self):
        return self.email
