from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_delete
from accounts.models import User
from notifications.models import Notification
from .models import Enrollment, Course
from student.models import Student

@receiver(post_save, sender=User)
def auto_enroll_intro_courses(sender, instance, created, **kwargs):
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
                birthday=timezone.now().date()  # Provide a default value for birthday
            )

        # Get the introductory courses
        intro_courses = Course.objects.filter(is_introductory=True)
        for course in intro_courses:
            Enrollment.objects.get_or_create(student=student, course=course)

@receiver(post_save, sender=Enrollment)
def send_course_full_email(sender, instance, created, **kwargs):
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


@receiver(post_delete, sender=Enrollment)
def send_enrollment_deletion_notification(sender, instance, **kwargs):
    try:
        student = instance.user
        course = instance.course
        message = f'You have been removed from the course: {course.name}.'
        Notification.objects.create(student=student, message=message)
    except User.DoesNotExist:
        print('User does not exist')
