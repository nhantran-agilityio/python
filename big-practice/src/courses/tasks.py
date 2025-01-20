from celery import shared_task
from datetime import datetime, timedelta
from .models import Course

@shared_task
def clean_up_inactive_courses():
    three_months_ago = datetime.now() - timedelta(days=90)
    inactive_courses = Course.objects.filter(is_active=False, updated_at__lt=three_months_ago)
    count = inactive_courses.count()
    inactive_courses.delete()
    return f"Deleted {count} inactive courses."
