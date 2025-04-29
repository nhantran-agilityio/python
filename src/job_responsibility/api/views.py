
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from ..models import JobResponsibility
from job_responsibility.api.serializers import JobResponsibilitySerializer


class JobResponsibilityViewSet(viewsets.ModelViewSet):
    queryset = JobResponsibility.objects.all()
    serializer_class = JobResponsibilitySerializer
    permission_classes = [IsAuthenticated]
