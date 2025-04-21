from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.job.serializers import JobSerializer
from .models import Job


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
