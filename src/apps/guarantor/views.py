from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from apps.accounts.models import User

from .models import Guarantor
from .serializers import GuarantorSerializer


class GuarantorDetailAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        guarantor = get_object_or_404(GuarantorSerializer, user=user)
        serializer = GuarantorSerializer(guarantor)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update guarantor details partially.",
        request_body=GuarantorSerializer,
        responses={
            200: GuarantorSerializer,
            400: "Invalid data provided."
        }
    )
    def patch(self, request, pk):
        guarantor = get_object_or_404(Guarantor, pk=pk)
        serializer = GuarantorSerializer(guarantor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Create a new contact",
        request_body=GuarantorSerializer,
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER,
                              description="Token: Bearer <access_token>",
                              type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request):
        serializer = GuarantorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        contact = get_object_or_404(Guarantor, pk=pk, user=request.user)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
