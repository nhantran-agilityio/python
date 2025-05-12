from django.forms import ValidationError
from core.api_views import BaseAuthenticatedModelViewSet
from guarantors.models import Guarantor
from .serializers import GuarantorSerializer


class GuarantorViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = GuarantorSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Guarantor.objects.none()
        return Guarantor.objects.filter(user=user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated to create a Guarantor.")
        serializer.save(user=self.request.user)
