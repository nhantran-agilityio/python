from django.contrib import admin
from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = (
       "user", "file_name", "file_path", "uploaded_at", "document_type"
    )


admin.site.register(Document, DocumentAdmin)
