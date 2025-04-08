from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "phone_num_1",
        "phone_num_2",
        "email",
        "city_of_residence",
        "residential_address",
    )


admin.site.register(Contact, ContactAdmin)
