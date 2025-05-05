from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from guarantor.models import Guarantor
from .serializers import GuarantorSerializer


class GuarantorViewSet(viewsets.ModelViewSet):
    serializer_class = GuarantorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Guarantor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
