import uuid
from django.db import models
from apps.accounts.models import User


class LeaveApplication(models.Model):
    LEAVE_TYPES = [
        ("Annual", "Annual"),
        ("Sick", "Sick"),
        ("Casual", "Casual"),
        ("Maternity", "Maternity"),
    ]
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    employee = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name="leave_applications")
    start_date = models.DateField()
    end_date = models.DateField()
    durations = models.IntegerField()
    resumption_date = models.DateField()
    reason = models.TextField()
    document_path = models.CharField(max_length=255, blank=True, null=True)
    relief_officer = models.ForeignKey(User, on_delete=models.SET_NULL,
                                       null=True, related_name="relief_officer")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EmployeeLeaveBalance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="leave_balances")
    leave_type = models.CharField(max_length=50)
    total_days = models.IntegerField()
