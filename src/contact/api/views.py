from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from drf_yasg.utils import swagger_auto_schema
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    resource_name = "contact"

    def get_contact(self, request):
        contact = getattr(request.user, 'contact', None)
        if not contact:
            raise NotFound("Contact not found.")
        return contact

    @swagger_auto_schema(responses={200: ContactSerializer})
    def list(self, request):
        contact = self.get_contact(request)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ContactSerializer,
        responses={200: ContactSerializer}
    )
    def partial_update(self, request, pk=None):
        contact = self.get_contact(request)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ContactSerializer,
        responses={201: ContactSerializer, 400: "Contact already exists"}
    )
    def create(self, request):
        if request.user.contact:
            raise ValidationError({"detail": "Contact already exists."})

        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()
        request.user.contact = contact
        request.user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


apps = [ContactViewSet]
