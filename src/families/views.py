from django.forms import ValidationError
from core.api_views import BaseAuthenticatedModelViewSet
from .models import Family
from .serializers import FamilySerializer


class FamilyViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = FamilySerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Family.objects.none()
        return Family.objects.filter(user=user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated to create a Family.")
        serializer.save(user=self.request.user)
