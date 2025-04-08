from django.contrib import admin
from .models import Education


class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "department",
        "course",
        "location",
        "start_date",
        "end_time",
        "description",
    )


admin.site.register(Education, EducationAdmin)
