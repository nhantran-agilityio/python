from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
from io import BytesIO
import zipfile

from documents.models import Document
from constants.enums import DocumentType
from documents.serializers import DocumentUploadSerializer
from utils.base import is_admin
from utils.conversions import camel_to_snake


class DocumentBaseView(APIView):
    permission_classes = [IsAuthenticated]

    def validate_document_type(self, doc_type_camel):
        doc_type = camel_to_snake(doc_type_camel)
        if not DocumentType.has_value(doc_type):
            raise ValidationError({"error": f"Invalid document type: {doc_type}"})
        return doc_type, None

    def extract_documents(self, request):
        documents = request.FILES
        if not documents:
            raise ValidationError({"error": "No documents provided."})
        return documents, None

    def parse_document_key(self, key):
        if key.startswith("documents[") and key.endswith("]"):
            return key[len("documents["):-1]
        return None


class MultipleDocumentUploadView(DocumentBaseView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Upload multiple documents with their types",
        manual_parameters=[
            openapi.Parameter(
                name=f"documents[{doc_type}]",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description=f"{doc_type.replace('_', ' ').title()} document"
            )
            for doc_type in DocumentType.values
        ],
        responses={201: "Files uploaded successfully!", 400: "Bad Request"}
    )
    def post(self, request, *args, **kwargs):
        documents, error_response = self.extract_documents(request)
        if error_response:
            raise ValidationError(detail=error_response.data)

        uploaded_files = []

        for key, file in documents.items():
            doc_type_camel = self.parse_document_key(key)
            if not doc_type_camel:
                raise ValidationError(detail={"error": f"Invalid key format: {key}"})

            doc_type, error_response = self.validate_document_type(doc_type_camel)
            if error_response:
                raise ValidationError(detail=error_response.data)

            document = Document.objects.create(
                user=request.user,
                document_file=file,
                document_type=doc_type
            )
            uploaded_files.append(DocumentUploadSerializer(document).data)

        return Response(
            {"message": "Files uploaded successfully!", "documents": uploaded_files},
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        operation_description="Update existing documents or upload new ones",
        manual_parameters=[
            openapi.Parameter(
                name=f"documents[{doc_type}]",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description=f"{doc_type.replace('_', ' ').title()} document"
            )
            for doc_type in DocumentType.values
        ],
        responses={200: "Documents updated successfully!", 400: "Bad Request", 404: "Document not found"}
    )
    def patch(self, request, *args, **kwargs):
        documents, error_response = self.extract_documents(request)
        if error_response:
            return error_response

        updated_files = []

        for key, file in documents.items():
            doc_type_camel = self.parse_document_key(key)
            if not doc_type_camel:
                raise ValidationError(detail={"error": f"Invalid key format: {key}"})

            doc_type, error_response = self.validate_document_type(doc_type_camel)
            if error_response:
                return error_response

            document, _ = Document.objects.update_or_create(
                user=request.user,
                document_type=doc_type,
                defaults={"document_file": file}
            )
            updated_files.append(DocumentUploadSerializer(document).data)

        return Response(
            {"message": "Documents updated successfully!", "documents": updated_files},
            status=status.HTTP_200_OK
        )


class DownloadAllDocumentsView(DocumentBaseView):
    def get(self, request, *args, **kwargs):
        documents = Document.objects.filter(user=request.user)

        if not documents.exists():
            raise NotFound("No documents found to download.")

        zip_filename = f"{request.user.username}_documents.zip"
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for document in documents:
                file_name = document.document_file.name.split("/")[-1]
                file_content = document.document_file.open().read()
                zip_file.writestr(file_name, file_content)

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'
        return response


class GetDocumentsAPIView(DocumentBaseView):
    @swagger_auto_schema(
        operation_description="Retrieve documents. Admins get all; users get only their own.",
        responses={
            200: openapi.Response(
                description="Documents retrieved successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_OBJECT)
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        documents = (
            Document.objects.all()
            if is_admin(request)
            else Document.objects.filter(user=request.user)
        )

        serializer = DocumentUploadSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
