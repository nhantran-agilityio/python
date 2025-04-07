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
                doc_type = key[len("documents["):-1]
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
        """
        # Query all documents for the authenticated user
        documents = Document.objects.filter(user=request.user)

        if not documents.exists():
            return Response(
                {"error": "No documents found for the user."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create a zip file in memory
        zip_filename = f"{request.user.username}_documents.zip"
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for document in documents:
                # Get the file path
                file_path = document.document_file.path
                # Add the file to the zip with its original name
                zip_file.write(file_path, os.path.basename(file_path))

        # Set the buffer's position to the beginning
        zip_buffer.seek(0)

        # Return the zip file as a response
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'
        return response
