import csv
from io import StringIO
from django.core.mail import EmailMessage
from celery import shared_task
from .models import LeaveApplication
from django.conf import settings


@shared_task
def send_monthly_leave_report():
    # Query leave history
    leave_history = LeaveApplication.objects.all()

    # Generate CSV
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(['Employee', 'Leave Type', 'Start Date', 'End Date', 'Status'])
    for leave in leave_history:
        writer.writerow([leave.employee.email, leave.type, leave.start_date, leave.end_date, leave.status])

    # Send email
    email = EmailMessage(
        subject='Monthly Leave Report',
        body='Please find the attached leave history report.',
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.ADMIN_EMAIL],
    )
    email.attach('leave_report.csv', csv_buffer.getvalue(), 'text/csv')
    email.send()
