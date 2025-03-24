from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.document.models import Document
from apps.document.seralizers import DocumentUploadSerializer


class MultipleDocumentUploadView(APIView):
    authentication_classes = [BasicAuthentication]
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Upload multiple documents",
        manual_parameters=[
            openapi.Parameter(
                'documents', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_FILE),
                description='List of document files to upload'
            ),
            openapi.Parameter(
                'document_type', openapi.IN_FORM, type=openapi.TYPE_STRING,
                description='List of document types corresponding to each file'
            ),
            openapi.Parameter(
                'user', openapi.IN_FORM, type=openapi.TYPE_STRING, description='User ID'
            ),
        ],
        responses={201: 'Files uploaded successfully!', 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('documents')
        document_types = request.data.getlist('document_type')
        user = request.data.get('user')

        if not files or not document_types:
            return Response({'error': 'Documents and document_type fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if len(files) != len(document_types):
            return Response({'error': 'Number of files must match number of document types'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_files = []
        for file, doc_type in zip(files, document_types):
            if doc_type not in dict(Document.DOCUMENT_TYPES):
                return Response({'error': f'Invalid document type: {doc_type}'}, status=status.HTTP_400_BAD_REQUEST)

            document = Document.objects.create(user_id=user, document_file=file, document_type=doc_type)
            uploaded_files.append(DocumentUploadSerializer(document).data)
