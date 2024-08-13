from django.contrib import admin
from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'point', 'description', "created_at")
    list_filter = ('course', 'student', 'created_at')


# Register your models here.
admin.site.register(Report, ReportAdmin)
