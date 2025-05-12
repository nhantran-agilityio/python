from django.contrib import admin

from .models import Guarantor


class GuarantorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "job",
        "phone",
    )


admin.site.register(Guarantor, GuarantorAdmin)
