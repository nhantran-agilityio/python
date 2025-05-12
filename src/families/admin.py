from django.contrib import admin
from .models import Family


class FamilyAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "relationship",
        "phone",
        "address"
    )


admin.site.register(Family, FamilyAdmin)
