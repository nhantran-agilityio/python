import os
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


class MultipleDocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Upload multiple documents with their types",
        manual_parameters=[
            openapi.Parameter(
                name="documents[offer_letter]",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Offer Letter document"
            ),
            openapi.Parameter(
                name="documents[birth_certificate]",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Birth Certificate document"
            ),
            openapi.Parameter(
                name="documents[guarantor_form]",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Guarantor Form document"
            ),
            openapi.Parameter(
                name="documents[degree_certificate]",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Degree Certificate document"
            ),
        ],
        responses={
            201: "Files uploaded successfully!",
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Handle bulk document upload where each document is associated with a type.
        """
        documents = request.FILES
        if not documents:
            return Response(
                {"error": "No documents provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_files = []
        for key, file in documents.items():
            # Extract the document type from the key (e.g., "documents[offer_letter]" -> "offer_letter")
            if key.startswith("documents[") and key.endswith("]"):
                doc_type_camel = key[len("documents["):-1]
                doc_type = camel_to_snake(doc_type_camel)
            else:
                return Response(
                    {"error": f"Invalid key format: {key}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate the document type
            if doc_type not in dict(Document.DOCUMENT_TYPES):
                return Response(
                    {"error": f"Invalid document type: {doc_type}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save the document
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


class DownloadAllDocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Download all documents uploaded by the authenticated user as a zip file.
        Returns a message if no documents are available.
        """
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
                file_path = document.document_file.path
                if os.path.exists(file_path):
                    zip_file.write(file_path, os.path.basename(file_path))

        zip_buffer.seek(0)

        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'
        return response


class GetDocumentsAPIView(APIView):
    """
    API to retrieve documents based on user role.
    Admins get all documents; regular users get only their own.
    """
    permission_classes = [IsAuthenticated]

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
        """
        Retrieve documents depending on the user role.
        """
        if request.user.role == "admin":
            documents = Document.objects.all()
        else:
            documents = Document.objects.filter(user=request.user)

        serializer = DocumentUploadSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
