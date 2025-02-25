from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
import csv
from django.conf import settings
from io import StringIO
from .models import Course


@shared_task
def clean_up_inactive_courses():
    """
    Deletes courses that have been inactive for more than 1 hour.
    """
    one_hour_ago = datetime.now() - timedelta(hours=1)
    deleted_count, _ = Course.objects.filter(
        is_active=False, updated_at__lt=one_hour_ago
    ).delete()
    return f"Deleted {deleted_count} inactive courses."


@shared_task
def send_monthly_report():
    """
    Sends a monthly report (a CSV file sent via email) sent to the instructor
    about the number of enrolled students per their course.

    """

    courses = Course.objects.all()
    for course in courses:
        instructors = course.instructors.all()
        student_count = course.enrollments.count()

        # Create CSV content
        csvfile = StringIO()
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Course Name', 'Number of Enrolled Students'])
        csvwriter.writerow([course.name, student_count])

        # Send email to each instructor
        for instructor in instructors:
            email = EmailMessage(
                'Monthly Enrollment Report',
                'Please find attached the monthly enrollment report.',
                settings.EMAIL_HOST_USER,
                [instructor.email],
            )
            email.attach(
                f'{course.name}_report.csv', csvfile.getvalue(), 'text/csv'
            )
            email.send()
