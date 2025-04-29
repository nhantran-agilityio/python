from django.contrib import admin
from .models import LeaveApplication


class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "type",
        "start_date",
        "end_date",
        "durations",
        "resumption_date",
        "reason",
        "document_path",
        "relief_officer",
        "status",
        "recall_status",
        "is_recalled",
        "recall_reason",
        "created_at",
        "updated_at",

    )


admin.site.register(LeaveApplication, LeaveApplicationAdmin)
