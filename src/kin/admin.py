from django.contrib import admin

from .models import Kin


class KinAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "job",
        "phone",
        "relationship",
        "residential_address",
    )


admin.site.register(Kin, KinAdmin)
