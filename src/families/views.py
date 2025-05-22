from core.api_views import BaseAuthenticatedModelViewSet
from core.custom_permissions import IsAdminOrOwner
from .models import Family
from .serializers import FamilySerializer


class FamilyViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = FamilySerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return Family.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
