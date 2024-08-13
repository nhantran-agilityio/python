from django.contrib import admin
from .models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "birthday",
        "gender",
        "email",
        "avatar",
        "address",
        "is_active",
    )
    search_fields = ("first_name", "last_name", "email")
    list_filter = ('courses', )


admin.site.register(Student, StudentAdmin)
