from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from drf_yasg import openapi
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from apps.kin.serializers import KinSerializer


class KinDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        kin = getattr(request.user, 'kin', None)
        if not kin:
            raise NotFound(detail="Kin not found.")

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
    def patch(self, request):
        kin = getattr(request.user, 'kin', None)
        if not kin:
            raise NotFound(detail="Kin not found.")

        serializer = KinSerializer(kin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Create a new kin",
        request_body=KinSerializer,
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER,
                              description="Token: Bearer <access_token>",
                              type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request):
        if request.user.kin:
            raise ValidationError({"detail": "kin already exists."})

        serializer = KinSerializer(data=request.data)
        if serializer.is_valid():
            kin = serializer.save()
            request.user.kin = kin
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
