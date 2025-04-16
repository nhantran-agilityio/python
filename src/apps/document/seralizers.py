from rest_framework import serializers
from djangorestframework_camel_case.util import underscore_to_camel
from .models import Document


class DocumentUploadSerializer(serializers.Serializer):
    documentType = serializers.ChoiceField(choices=Document.DOCUMENT_TYPES)
    documentFile = serializers.FileField(source='document_file')

    class Meta:
        model = Document
        fields = ['id', 'user', 'documentType', 'documentFile']

    def get_documentType(self, obj):
        return underscore_to_camel(obj.document_type)
