from rest_framework import serializers

from apps.accounts.models import User
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'user', 'document_type', 'document_file', 'uploaded_at']


class DocumentUploadSerializer(serializers.Serializer):
    document_file = serializers.FileField()
    document_type = serializers.ChoiceField(choices=Document.DOCUMENT_TYPES)


class MultipleDocumentUploadSerializer(serializers.Serializer):
    documents = DocumentUploadSerializer(many=True)

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        documents_data = validated_data.pop('documents')
        user = validated_data.pop('user')
        document_instances = []
        for document_data in documents_data:
            document_instance = Document.objects.create(
                user=user,
                document_type=document_data['document_type'],
                document_file=document_data['document_file']
            )
            document_instances.append(document_instance)
        return document_instances
