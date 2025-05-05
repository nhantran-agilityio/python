from rest_framework import serializers
from constants.enums import DocumentType
from document.models import Document


class DocumentUploadSerializer(serializers.Serializer):
    document_file = serializers.FileField()
    document_type = serializers.ChoiceField(choices=DocumentType.choices)
    documentFile = serializers.FileField(source='document_file')

    class Meta:
        model = Document
        fields = ['id', 'user', 'document_type', 'documentFile']
