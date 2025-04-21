
from rest_framework import generics
from .models import JobResponsibility
from apps.job_responsibility.serializers import JobResponsibilitySerializer


class JobResponsibilityListCreateView(generics.ListCreateAPIView):
    queryset = JobResponsibility.objects.all()
    serializer_class = JobResponsibilitySerializer


class JobResponsibilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobResponsibility.objects.all()
    serializer_class = JobResponsibilitySerializer
