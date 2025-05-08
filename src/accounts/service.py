from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from urllib.parse import urlencode


class UserRegistrationService:
    @staticmethod
    def register_user(serializer):
        """
        Register a new user.

        This method saves the user instance returned by the serializer and
        sends an activation email to the user.

        :param serializer: The serializer for the user.
        :type serializer: accounts.serializers.RegisterSerializer
        :return: The newly created user instance.
        :type: accounts.models.User
        """
        user = serializer.save(is_active=False)
        UserRegistrationService.send_activation_email(user)
        return user

    @staticmethod
    def send_activation_email(user):
        """
        Send an activation email to the user.

        This method renders an email using the ``email/activation_email.txt``
        template and sends it to the user's email address. The email contains a
        link to the frontend's activation view, which includes the user's
        ``uidb64`` and the default token generator's token for the user.

        :param user: The user to send the activation email to.
        :type user: accounts.models.User
        """

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = (
            f"{settings.FE_DOMAIN}?"
            f"{urlencode({'uidb64': uid, 'token': token})}"
        )

        message = render_to_string('email/activation_email.txt', {
            'user': user,
            'domain': activation_link,
        })

        email = EmailMessage(
            subject='Activate your account.',
            body=message,
            to=[user.email]
        )
        email.send()
