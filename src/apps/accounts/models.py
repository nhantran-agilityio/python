from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from apps.contact.models import Contact
from apps.job.models import Job
from apps.kin.models import Kin


def user_avatar_upload(instance, filename):
    """
    Generate a dynamic file path for user avatars.
    """
    return f'avatars/{instance.id}/{filename}'


class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    CANDIDATE = "candidate", "Candidate"
    EMPLOYEE = "employee", "Employee"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        blank=True,
        null=True
    )
    is_receive_newsletters = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(
        upload_to=user_avatar_upload,
        null=True,
        blank=True
    )
    job = models.ForeignKey(
        Job,
        related_name='users',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    contact = models.ForeignKey(
        Contact,
        related_name='users',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    kin = models.ForeignKey(
        Kin,
        related_name='users',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
