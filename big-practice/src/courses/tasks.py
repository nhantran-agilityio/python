from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import csv
from django.conf import settings
from io import StringIO
from .models import Course


@shared_task
def clean_up_inactive_courses():
    # days=90 use for 3 months
    """
    Delete courses that have been inactive for more than 1 hour.
    """

    one_hour_ago = datetime.now() - timedelta(hours=1)
    inactive_courses = Course.objects.filter(
        is_active=False, updated_at__lt=one_hour_ago)
    count = inactive_courses.count()
    inactive_courses.delete()
    return f"Deleted {count} inactive courses."


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


def create_periodic_task():
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='0',
        day_of_month='1',
        month_of_year='*',
        day_of_week='*',
    )

    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name='Send Monthly Report',
        task='courses.tasks.send_monthly_report',
    )
