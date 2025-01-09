from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User
from courses.models import Course, Enrollment

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def auto_enroll_new_user(sender, instance, created, **kwargs):
    if created:
        # Get the introductory courses
        intro_courses = Course.objects.filter(is_introductory=True)
        for course in intro_courses:
            Enrollment.objects.create(user=instance, course=course)
