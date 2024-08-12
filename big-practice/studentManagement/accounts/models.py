from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, models.Model):
    """
    Custom User model for the authentication system.

    Attributes:
        email (str): The email address of the user.
        username (str): The username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        is_active (bool): Indicates whether the user account is active.
        created_at (datetime): The date and time when the user account was
        created.
        updated_at (datetime): The date time when account as last updated.
    """

    email = models.EmailField(unique=True)
    is_Admin = models.BooleanField(
        default=False,
        help_text="When true, the user can log in this admin site. \
            Otherwise, we can only access the API.",
    )

    def __str__(self) -> str:
        """
        Returns the string representation of the User instance.
        """
        return self.email
