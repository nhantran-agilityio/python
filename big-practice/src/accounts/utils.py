from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    A token generator class for email verification.

    This class inherits from PasswordResetTokenGenerator and is used to generate
    and validate tokens for email verification purposes. It does not add any
    additional functionality to the base class but serves as a specific
    implementation for email verification.
    """
    pass


email_verification_token = EmailVerificationTokenGenerator()
