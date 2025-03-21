from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Document
from apps.document.seralizers import DocumentSerializer
from rest_framework.decorators import api_view


class DocumentUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @api_view(['POST'])
    def post(self, request, *args, **kwargs):
        user = request.user
        files = request.FILES.getlist('files')
        document_type = request.data.get('document_type')

        if not files:
            return Response({"error": "No files uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        if not document_type:
            return Response({"error": "Document type is required."}, status=status.HTTP_400_BAD_REQUEST)

        documents = []
        for file in files:
            document = Document(user=user, document_type=document_type, file=file)
            document.save()
            documents.append(document)

        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
