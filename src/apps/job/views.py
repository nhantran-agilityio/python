from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from apps.job.seralizers import JobSerializer
from .models import Job


class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobByUserView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def job_list_by_user(request, user_id):
        try:
            jobs = Job.objects.filter(user_id=user_id)
            job_data = [{"id": job.id, "title": job.title} for job in jobs]
            return JsonResponse(job_data, safe=False)
        except Job.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
