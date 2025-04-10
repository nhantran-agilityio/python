from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.leave_application.models import LeaveApplication
from .models import Notification


@receiver(post_save, sender=LeaveApplication)
def send_leave_recall_notification(sender, instance, created, **kwargs):
    if instance.is_recalled:
        Notification.objects.create(
            user=instance.employee,
            message=(
                f"Your {instance.type} leave has been recalled by "
                f"{instance.relief_officer}. Please return before "
                f"{instance.end_date}."
            )
        )
