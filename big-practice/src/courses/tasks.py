from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now
import csv
import io

from .models import Course

# @shared_task
# def clean_up_inactive_courses():
#     three_months_ago = datetime.now() - timedelta(days=90)
#     inactive_courses = Course.objects.filter(is_active=False, updated_at__lt=three_months_ago)
#     count = inactive_courses.count()
#     inactive_courses.delete()
#     return f"Deleted {count} inactive courses."


@shared_task
def clean_up_inactive_courses():
    one_hour_ago = datetime.now() - timedelta(hours=1)
    inactive_courses = Course.objects.filter(
        is_active=False, updated_at__lt=one_hour_ago)
    count = inactive_courses.count()
    inactive_courses.delete()
    return f"Deleted {count} inactive courses."


@shared_task
def send_daily_report():
    # Get the current date
    current_date = now().date()

    # Create a CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Course Name', 'Instructor', 'Number of Enrolled Students'])

    # Get all courses and their enrollments
    courses = Course.objects.all()
    for course in courses:
        instructors = ", ".join([instructor.name for instructor in course.instructors.all()])
        num_enrollments = course.enrollments.count()
        writer.writerow([course.name, instructors, num_enrollments])

    # Get the CSV content
    csv_content = output.getvalue()
    output.close()

    # Send the email to each instructor
    for course in courses:
        for instructor in course.instructors.all():
            subject = f'Daily Enrollment Report - {current_date}'
            message = render_to_string('courses/daily_report_email.html', {
                'instructor': instructor,
                'current_date': current_date,
            })
            email = EmailMessage(subject, message, to=[instructor.email])
            email.attach(f'enrollment_report_{current_date}.csv', csv_content, 'text/csv')
            email.send()
