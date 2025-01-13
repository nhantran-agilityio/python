from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Student


@receiver(post_save, sender=Student)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our System'
        message = f'Hi {instance.first_name},\n\nWelcome to our system! We are excited to have you on board.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)
