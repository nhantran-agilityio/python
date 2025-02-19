from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_delete
from accounts.models import User
from notifications.models import Notification
from .models import Enrollment, Course
from student.models import Student
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def auto_enroll_intro_courses(sender, instance, created, **kwargs):
    """
    Signal receiver that auto-enrolls new users in all introductory courses.

    Args:
        sender (User): The model class that sent the signal.
        instance (User): The instance of the model class that sent the signal.
        created (bool): A boolean indicating whether the user instance was
            created.
    """
    if created:  # Trigger only for new users
        # Ensure the instance is a Student
        try:
            student = Student.objects.get(user=instance)
        except Student.DoesNotExist:
            student = Student.objects.create(
                user=instance,
                first_name=instance.first_name,
                last_name=instance.last_name,
                email=instance.email,
                # Provide a default value for birthday
                birthday=timezone.now().date()
            )

        # Get the introductory courses
        intro_courses = Course.objects.filter(is_introductory=True)
        for course in intro_courses:
            Enrollment.objects.get_or_create(student=student, course=course)

            if created:
                logger.info(
                    f"Student {student.email} enrolled in course {course.name}"
                )

@receiver(post_save, sender=Enrollment)
def send_course_full_email(sender, instance, created, **kwargs):
    """
    Signal receiver that sends an email to the course instructors
    when a course has reached its enrollment limit.

    Args:
        sender (Enrollment): The model class that sent the signal.
        instance (Enrollment): The instance of the model class that sent
            the signal.
        created (bool): A boolean indicating whether the enrollment instance
            was created.
        **kwargs: Additional keyword arguments passed to the signal handler.
    """
    if created:
        course = instance.course
        if course.is_full:
            subject = 'Course Enrollment Limit Reached'
            message = (
                f'The course "{course.name}" has reached its enrollment limit.'
            )
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [instructor.email for instructor
                              in course.instructors.all()]
            send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Enrollment)
def send_enrollment_notification(sender, instance, created, **kwargs):
    """
    Signal receiver that sends a notification to the course instructors
    when a student enrolls in a course.

    Args:
        sender (Enrollment): The model class that sent the signal.
        instance (Enrollment): The instance of the model class that sent
            the signal.
        created (bool): A boolean indicating whether the enrollment instance was created.
        **kwargs: Additional keyword arguments passed to the signal handler.

    """
    if created:
        course = instance.course
        student = instance.student
        message = (
            f'{student.first_name} has enrolled in your course: {course.name}.'
        )
        for instructor in course.instructors.all():
            if instructor.user:  # Ensure the instructor has a user
                Notification.objects.create(
                    user=instructor.user, message=message
                )


@receiver(post_delete, sender=Enrollment)
def send_enrollment_deletion_notification(sender, instance, **kwargs):
    """
    Signal receiver that sends a notification to the student when their
    enrollment is deleted.

    Args:
        sender (Enrollment): The model class that sent the signal.
        instance (Enrollment): The instance of the model class that sent
            the signal.
        **kwargs: Additional keyword arguments passed to the signal handler.

    """
    student = instance.student
    course = instance.course
    message = f'You have been removed from the course: {course.name}.'
    try:
        Notification.objects.create(user=student.user, message=message)
    except User.DoesNotExist:
        logger.error(f"User for student {student.email} does not exist.")
