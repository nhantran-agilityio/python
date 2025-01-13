from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Enrollment

@receiver(post_save, sender=Enrollment)
def send_course_full_email(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        if course.is_full:
            subject = 'Course Enrollment Limit Reached'
            message = f'The course "{course.name}" has reached its enrollment limit.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [instructor.email for instructor
                              in course.instructors.all()]
            send_mail(subject, message, from_email, recipient_list)
