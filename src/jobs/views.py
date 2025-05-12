from core.api_views import BaseAuthenticatedModelViewSet
from jobs.models import Job
from jobs.serializers import JobSerializer


class JobViewSet(BaseAuthenticatedModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
