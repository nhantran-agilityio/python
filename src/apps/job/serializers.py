from rest_framework import serializers

from apps.job_responsibility.serializers import JobResponsibilitySerializer
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    responsibilities = JobResponsibilitySerializer(many=True, read_only=True)
    line_management_full_name = serializers.SerializerMethodField()
    id = serializers.UUIDField(required=False)

    class Meta:
        model = Job
        fields = [
            'id', 'name', 'description', 'department',
            'job_category',
            'responsibilities', 'line_management_full_name'
        ]

    def get_line_management_full_name(self, obj):
        if isinstance(obj, Job):
            return obj.get_line_management()
        return None
