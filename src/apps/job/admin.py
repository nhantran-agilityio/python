from django.contrib import admin
from .models import Job


class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "department",
        "line_management",
        "job_category",
    )
    search_fields = ("first_name", "last_name", "email")


admin.site.register(Job, JobAdmin)
