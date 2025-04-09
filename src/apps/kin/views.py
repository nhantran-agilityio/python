from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from apps.accounts.models import User
from .models import Kin
from .serializers import KinSerializer


class KinDetailAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        kin = get_object_or_404(KinSerializer, user=user)

        serializer = KinSerializer(kin)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update kin details partially.",
        request_body=KinSerializer,
        responses={
            200: KinSerializer,
            400: "Invalid data provided."
        }
    )
    def patch(self, request, pk):
        kin = get_object_or_404(Kin, pk=pk)
        serializer = KinSerializer(kin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Create a new contact",
        request_body=KinSerializer,
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER,
                              description="Token: Bearer <access_token>",
                              type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request):
        serializer = KinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
