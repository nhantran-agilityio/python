from rest_framework.exceptions import ValidationError
from io import BytesIO
import zipfile
from documents.models import Document
from documents.serializers import DocumentUploadSerializer
from constants.enums import DocumentType
from core.conversions import camel_to_snake


class DocumentService:
    @staticmethod
    def validate_document_type(doc_type_camel):
        doc_type = camel_to_snake(doc_type_camel)
        if not DocumentType.has_value(doc_type):
            raise ValidationError({"error": f"Invalid document type: {doc_type}"})
        return doc_type

    @staticmethod
    def parse_document_key(key):
        if key.startswith("documents[") and key.endswith("]"):
            return key[len("documents["):-1]
        raise ValidationError({"error": f"Invalid key format: {key}"})

    @staticmethod
    def upload_documents(user, documents):
        uploaded_files = []
        for key, file in documents.items():
            doc_type_camel = DocumentService.parse_document_key(key)
            doc_type = DocumentService.validate_document_type(doc_type_camel)

            document = Document.objects.create(
                user=user,
                document_file=file,
                document_type=doc_type
            )
            uploaded_files.append(DocumentUploadSerializer(document).data)
        return uploaded_files

    @staticmethod
    def update_documents(user, documents):
        updated_files = []
        for key, file in documents.items():
            doc_type_camel = DocumentService.parse_document_key(key)
            doc_type = DocumentService.validate_document_type(doc_type_camel)

            document, _ = Document.objects.update_or_create(
                user=user,
                document_type=doc_type,
                defaults={"document_file": file}
            )
            updated_files.append(DocumentUploadSerializer(document).data)
        return updated_files


class ZipService:
    @staticmethod
    def create_zip_from_documents(documents):
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            for document in documents:
                file_name = document.document_file.name.rsplit("/", 1)[-1]
                with document.document_file.open('rb') as file:
                    zip_file.writestr(file_name, file.read())
        zip_buffer.seek(0)
        return zip_buffer
