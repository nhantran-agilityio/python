from rest_framework import serializers

from job_responsibility.models import JobResponsibility


class JobResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResponsibility
        fields = '__all__'
