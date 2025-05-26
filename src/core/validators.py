from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from constants.error_messages import ErrorMessage


User = get_user_model()


def validate_email(email):
    """
    Validate that the email is unique.
    """

    if User.objects.filter(email=email).exists():
        raise ValidationError(ErrorMessage.EMAIL_EXISTS)
    return email
