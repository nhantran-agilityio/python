from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Family
from .serializers import FamilySerializer


class FamilyViewSet(viewsets.ModelViewSet):
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Family.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
