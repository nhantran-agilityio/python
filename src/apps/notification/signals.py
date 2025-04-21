from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.leave_application.models import LeaveApplication
from apps.notification.models import Notification


@receiver(post_save, sender=LeaveApplication)
def send_leave_recall_notification(sender, instance, created, **kwargs):
    if instance.is_recalled and instance.recall_status == "Pending":
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
