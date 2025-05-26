import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from constants.error_messages import ErrorMessage

SPECIAL_CHARACTER_REGEX = r"[!@#$%^&*(),.?\":{}|<>]"


class SpecialCharacterValidator:
    def validate(self, password, user=None):
        if not re.search(r"[A-Z]", password):
            raise ValidationError(_(ErrorMessage.PASSWORD_UPPERCASE),
                                  code="password_no_upper")
        if not re.search(r"[a-z]", password):
            raise ValidationError(_(ErrorMessage.PASSWORD_LOWERCASE),
                                  code="password_no_lower")
        if not re.search(r"\d", password):
            raise ValidationError(_(ErrorMessage.PASSWORD_NUMBER),
                                  code="password_no_digit")
        if not re.search(SPECIAL_CHARACTER_REGEX, password):
            raise ValidationError(_(ErrorMessage.PASSWORD_SPECIAL_CHAR),
                                  code="password_no_special")

    def get_help_text(self):
        return _(ErrorMessage.PASSWORD_INVALID)


def validate_phone_number(phone_number):
    """
    Validate the phone number to ensure it contains only digits and is of
    valid length.
    """

    if not phone_number:
        return

    if not phone_number.isdigit():
        raise ValidationError(ErrorMessage.PHONE_NUMBER_ONLY_NUMBER)
    if len(phone_number) < 10 or len(phone_number) > 11:
        raise ValidationError(ErrorMessage.PHONE_NUMBER_INVALID_LENGTH)
    return phone_number
