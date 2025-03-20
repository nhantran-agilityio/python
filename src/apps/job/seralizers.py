from rest_framework import serializers
from apps.document.seralizers import DocumentSerializer
from apps.job_responsibility.seralizers import JobResponsibilitySerializer
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    responsibilities = JobResponsibilitySerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
