from core.api_views import BaseAuthenticatedModelViewSet
from jobs.models import Job
from jobs.serializers import JobSerializer
from core.custom_permissions import IsAdminOrOwner


class JobViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
