from core.api_views import BaseAuthenticatedModelViewSet
from guarantors.models import Guarantor
from .serializers import GuarantorSerializer


class GuarantorViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = GuarantorSerializer

    def get_queryset(self):
        return Guarantor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
