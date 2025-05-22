from core.api_views import BaseAuthenticatedModelViewSet
from core.custom_permissions import IsAdminOrOwner
from guarantors.models import Guarantor
from .serializers import GuarantorSerializer


class GuarantorViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = GuarantorSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return Guarantor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
