from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os

from apps.job.models import Job


def user_avatar_upload(instance, filename):
    """Generate file path for new avatar upload"""
    ext = filename.split('.')[-1]
    filename = f'{instance.id}.{ext}'
    return os.path.join('avatars/', filename)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=50, null=True, blank=True)
    is_receive_newsletters = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to=user_avatar_upload, null=True, blank=True)
    job = models.ForeignKey(Job, related_name='users', on_delete=models.CASCADE, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
