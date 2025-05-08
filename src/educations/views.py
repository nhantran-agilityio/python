from core.api_views import BaseAuthenticatedModelViewSet
from educations.models import Education
from .serializers import EducationSerializer


class EducationViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = EducationSerializer

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
