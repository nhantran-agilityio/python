from django.contrib import admin
from .models import BankAccount


class FinancialAdmin(admin.ModelAdmin):
    list_display = (
        "bank_name",
        "account_no",
        "account_name",
    )


admin.site.register(BankAccount, FinancialAdmin)
