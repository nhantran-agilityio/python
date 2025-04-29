from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Financial
from .serializers import FinancialSerializer


class FinancialViewSet(viewsets.ModelViewSet):
    serializer_class = FinancialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Financial.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
