from django.contrib import admin
from .models import User


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "username",
        "email",
        "is_active",
        "role",
        "phone"
    )
    search_fields = ("first_name", "last_name", "email")


admin.site.register(User, AccountAdmin)
