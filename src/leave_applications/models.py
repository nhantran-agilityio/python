from django.db import models
from accounts.models import User
from constants.enums import LeaveStatus, LeaveType
from core.models import AbstractBaseModel


class LeaveApplication(AbstractBaseModel):
    type = models.CharField(
        max_length=20,
        choices=LeaveType.choices,
        default=LeaveType.ANNUAL
    )
    employee = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name="leave_applications")
    start_date = models.DateField()
    end_date = models.DateField()
    durations = models.IntegerField()
    resumption_date = models.DateField()
    reason = models.TextField()
    document_path = models.FileField(upload_to='documents/', blank=True, null=True)
    relief_officer = models.ForeignKey(User, on_delete=models.SET_NULL,
                                       null=True, related_name="relief_officer")
    status = models.CharField(
        max_length=20,
        choices=LeaveStatus.choices,
        default=LeaveStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recall_status = models.CharField(
        max_length=20,
        choices=LeaveStatus.choices,
        default=LeaveStatus.PENDING
    )
    recall_reason = models.TextField(blank=True, null=True)
    recall_date = models.DateField(blank=True, null=True)
    is_recalled = models.BooleanField(default=False)
    new_resumption_date = models.DateField(blank=True, null=True)
    days_remaining = models.PositiveIntegerField(blank=True, null=True)
    recalled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recalls_made')
    recall_deadline = models.DateField(null=True, blank=True)

    @property
    def is_pending_recall(self):
        return self.recall_status == LeaveStatus.PENDING
