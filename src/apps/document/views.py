from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import zipfile
from io import BytesIO
from django.http import HttpResponse
from apps.document.models import Document
from apps.document.seralizers import DocumentUploadSerializer
from utils.conversions import camel_to_snake


class DocumentBaseView(APIView):
    permission_classes = [IsAuthenticated]

    def validate_document_type(self, doc_type_camel):
        doc_type = camel_to_snake(doc_type_camel)
        if doc_type not in dict(Document.DOCUMENT_TYPES):
            return None, Response(
                {"error": f"Invalid document type: {doc_type}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return doc_type, None


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
            for doc_type in dict(Document.DOCUMENT_TYPES).keys()
        ],
        responses={
            201: "Files uploaded successfully!",
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        documents = request.FILES
        if not documents:
            return Response(
                {"error": "No documents provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_files = []
        for key, file in documents.items():
            if key.startswith("documents[") and key.endswith("]"):
                doc_type_camel = key[len("documents["):-1]
                doc_type, error_response = self.validate_document_type(doc_type_camel)
                if error_response:
                    return error_response
            else:
                return Response(
                    {"error": f"Invalid key format: {key}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            document = Document.objects.create(
                user=request.user,
                document_file=file,
                document_type=doc_type
            )
            uploaded_files.append(DocumentUploadSerializer(document).data)

        return Response(
            {
                "message": "Files uploaded successfully!",
                "documents": uploaded_files,
            },
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        operation_description="Update a specific document by type",
        manual_parameters=[
            openapi.Parameter(
                name="documentType",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Type of the document to update"
            ),
            openapi.Parameter(
                name="documentFile",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="New document file"
            ),
        ],
        responses={
            200: "Document updated successfully!",
            400: "Bad Request",
            404: "Document not found"
        }
    )
    def patch(self, request, *args, **kwargs):
        doc_type_camel = request.data.get("documentType")
        file = request.FILES.get("documentFile")

        if not doc_type_camel or not file:
            return Response(
                {"error": "Both documentType and documentFile are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        doc_type, error_response = self.validate_document_type(doc_type_camel)
        if error_response:
            return error_response

        try:
            document = Document.objects.get(user=request.user, document_type=doc_type)
            document.document_file = file
            document.save()
        except Document.DoesNotExist:
            return Response(
                {"error": "Document not found for this type."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "message": "Document updated successfully!",
                "document": DocumentUploadSerializer(document).data
            },
            status=status.HTTP_200_OK
        )


class DownloadAllDocumentsView(DocumentBaseView):
    def get(self, request, *args, **kwargs):
        documents = Document.objects.filter(user=request.user)

        if not documents.exists():
            return Response(
                {"message": "No documents found to download."},
                status=status.HTTP_200_OK
            )

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
        operation_description=(
            "Retrieve documents. Admins get all; "
            "users get only their own."
        ),
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
            if request.user.role == "admin"
            else Document.objects.filter(user=request.user)
        )

        serializer = DocumentUploadSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
