from django.contrib import admin
from .models import JobResponsibility


class JobResponsibilityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "job",
        "description",
    )
    search_fields = ("first_name", "last_name", "email")


admin.site.register(JobResponsibility, JobResponsibilityAdmin)
