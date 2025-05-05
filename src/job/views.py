from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from job.models import Job
from job.serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
