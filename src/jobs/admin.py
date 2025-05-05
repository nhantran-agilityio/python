from django.contrib import admin
from .models import Job


class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "department",
        "get_line_management",
        "job_category",
    )
    search_fields = ("first_name", "last_name", "email")

    def get_line_management(self, obj):
        return obj.get_line_management()


admin.site.register(Job, JobAdmin)
