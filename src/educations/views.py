from core.api_views import BaseAuthenticatedModelViewSet
from core.custom_permissions import IsAdminOrOwner
from educations.models import Education
from .serializers import EducationSerializer


class EducationViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
