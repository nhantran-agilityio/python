from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Guarantor
from .serializers import GuarantorSerializer


class GuarantorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Guarantor instances.
    """
    serializer_class = GuarantorSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response({
                "message": "No Guarantor found with the given ID.",
                "data": None
            }, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response({
            "message": "Success",
            "data": serializer.data
        })

    def get_queryset(self):
        return Guarantor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
