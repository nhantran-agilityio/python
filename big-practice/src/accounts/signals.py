from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from notifications.models import Notification
from courses.models import Course, Enrollment
from student.models import Student

@receiver(post_save, sender=Enrollment)
def send_enrollment_notification(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        student = instance.student
        message = (
            f'{student.first_name} has enrolled in your course: {course.name}.'
        )
        for instructor in course.instructors.all():
            if instructor.user:  # Ensure the instructor has a user
                Notification.objects.create(user=instructor.user, message=message)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def auto_enroll_new_user(sender, instance, created, **kwargs):
#     if created:
#         # Ensure the instance is a Student
#         student, created = Student.objects.get_or_create(
#             user=instance,
#             defaults={
#                 'first_name': instance.first_name,
#                 'last_name': instance.last_name,
#                 'email': instance.email,
#                 'birthday': timezone.now().date()
#             }
#         )

#         # Check if the student was created or already exists
#         if not student:
#             return

#         # Get the introductory courses
#         intro_courses = Course.objects.filter(is_introductory=True)
#         for course in intro_courses:
#             Enrollment.objects.get_or_create(student=student, course=course)
