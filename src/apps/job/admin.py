from django.contrib import admin
from .models import Job


class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "role",
        "department",
        "line_management",
    )
    search_fields = ("first_name", "last_name", "email")


admin.site.register(Job, JobAdmin)
