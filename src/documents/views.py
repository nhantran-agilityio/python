# views.py
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
from rest_framework.exceptions import NotFound
from constants.enums import DocumentType
from core.responses import ApiResponse
from documents.models import Document
from documents.serializers import DocumentUploadSerializer
from documents.services import DocumentService, ZipService


class MultipleDocumentUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Upload multiple documents with their types",
        manual_parameters=[
            openapi.Parameter(
                name=f"documents[{doc_type}]",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description=f"{doc_type.replace('_', ' ').title()} document"
            ) for doc_type in DocumentType.values
        ],
        responses={201: "Files uploaded successfully!", 400: "Bad Request"}
    )
    def post(self, request):
        uploaded_files = DocumentService.upload_documents(request.user, request.FILES)
        return ApiResponse(
            message="Files uploaded successfully!",
            status_code=status.HTTP_201_CREATED,
            data={"documents": uploaded_files}
        )

    @swagger_auto_schema(
        operation_description="Update existing documents or upload new ones",
        manual_parameters=[
            openapi.Parameter(
                name=f"documents[{doc_type}]",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description=f"{doc_type.replace('_', ' ').title()} document"
            ) for doc_type in DocumentType.values
        ],
        responses={200: "Documents updated successfully!", 400: "Bad Request"}
    )
    def patch(self, request):
        updated_files = DocumentService.update_documents(request.user, request.FILES)
        return ApiResponse(
            message="Documents updated successfully!",
            status_code=status.HTTP_200_OK,
            data={"documents": updated_files}
        )


class DownloadAllDocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        documents = Document.objects.filter(
            user=request.user
        ).only("document_file")

        if not documents.exists():
            raise NotFound("No documents found to download.")

        zip_buffer = ZipService.create_zip_from_documents(documents)
        zip_filename = f"{request.user.username}_documents.zip"

        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = (
            f'attachment; filename="{zip_filename}"'
        )
        return response


class GetDocumentsAPIView(APIView):
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
    def get(self, request):
        documents = (
            Document.objects.all()
            if request.user.is_admin
            else Document.objects.filter(user=request.user)
        )
        serializer = DocumentUploadSerializer(documents, many=True)
        return ApiResponse(
            message="Documents retrieved successfully.",
            status_code=status.HTTP_200_OK,
            data={"documents": serializer.data}
        )
