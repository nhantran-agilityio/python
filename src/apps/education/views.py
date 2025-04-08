from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from apps.accounts.models import User

from .models import Education
from .serializers import EducationSerializer


class EducationDetailAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        education = get_object_or_404(Education, user=user)
        serializer = EducationSerializer(education)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update education details partially.",
        request_body=EducationSerializer,  # Use the serializer to define the request body
        responses={
            200: EducationSerializer,
            400: "Invalid data provided."
        }
    )
    def patch(self, request, pk):
        education = get_object_or_404(Education, pk=pk)
        serializer = EducationSerializer(education, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

