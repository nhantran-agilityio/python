from django.db.models.signals import post_save
from django.dispatch import receiver

from leave_application.models import LeaveApplication
from notifications.models import Notification
from utils.base import is_pending_recall


@receiver(post_save, sender=LeaveApplication)
def send_leave_recall_notification(sender, instance, created, **kwargs):
    if is_pending_recall(instance):
        relief_officer = instance.relief_officer
        full_name = f"{relief_officer.first_name} {relief_officer.last_name}" if relief_officer else "an unknown officer"

        Notification.objects.create(
            user=instance.employee,
            recall_id=instance.id,
            message=(
                f"Your {instance.type} leave has been recalled by "
                f"{full_name}. Please return before "
                f"{instance.end_date}."
            )
        )
