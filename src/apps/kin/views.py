from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Kin
from .serializers import KinSerializer


class KinViewSet(viewsets.ModelViewSet):
    serializer_class = KinSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Kin.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
