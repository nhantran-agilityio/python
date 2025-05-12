from django.forms import ValidationError
from core.api_views import BaseAuthenticatedModelViewSet
from educations.models import Education
from .serializers import EducationSerializer


class EducationViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = EducationSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Education.objects.none()
        return Education.objects.filter(user=user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated to create a Education.")
        serializer.save(user=self.request.user)
