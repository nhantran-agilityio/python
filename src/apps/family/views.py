from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from apps.accounts.models import User
from .models import Family
from .serializers import FamilySerializer


class FamilyDetailAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        family = get_object_or_404(Family, user=user)
        serializer = FamilySerializer(family)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update family details partially.",
        request_body=FamilySerializer,
        responses={
            200: FamilySerializer,
            400: "Invalid data provided."
        }
    )
    def patch(self, request, pk):
        family = get_object_or_404(Family, pk=pk)
        serializer = FamilySerializer(family, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Create a new contact",
        request_body=FamilySerializer,
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER,
                              description="Token: Bearer <access_token>",
                              type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request):
        serializer = FamilySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        contact = get_object_or_404(Family, pk=pk, user=request.user)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
