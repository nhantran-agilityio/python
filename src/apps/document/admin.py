from django.contrib import admin
from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = (
       "job", "file_name", "file_path", "uploaded_at"
    )


admin.site.register(Document, DocumentAdmin)
