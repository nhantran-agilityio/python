from core.api_views import BaseAuthenticatedModelViewSet
from kins.models import Kin
from kins.serializers import KinSerializer
from core.custom_permissions import IsAdminOrOwner


class KinViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = KinSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return Kin.objects.visible_to(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
