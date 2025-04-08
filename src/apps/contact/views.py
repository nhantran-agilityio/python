from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from apps.accounts.models import User
from .models import Contact
from .serializers import ContactSerializer


class ContactDetailAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        contact = get_object_or_404(Contact, user=user)
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
    def patch(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
