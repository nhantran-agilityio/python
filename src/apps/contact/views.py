from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from drf_yasg import openapi
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import ContactSerializer


class ContactDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        contact = getattr(request.user, 'contact', None)
        if not contact:
            raise NotFound(detail="Contact not found.")

        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update contact details partially.",
        request_body=ContactSerializer,
        responses={
            200: ContactSerializer,
            400: "Invalid data provided."
        }
    )
    def patch(self, request):
        contact = getattr(request.user, 'contact', None)
        if not contact:
            raise NotFound(detail="Contact not found.")

        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Create a new contact",
        request_body=ContactSerializer,
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER,
                              description="Token: Bearer <access_token>",
                              type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request):
        if request.user.contact:
            raise ValidationError({"detail": "Contact already exists."})

        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            request.user.contact = contact
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
