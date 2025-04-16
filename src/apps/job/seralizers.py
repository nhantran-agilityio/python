from rest_framework import serializers
from apps.accounts.models import User
from apps.job_responsibility.seralizers import JobResponsibilitySerializer
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    responsibilities = JobResponsibilitySerializer(many=True, read_only=True)
    line_management_full_name = serializers.SerializerMethodField()
    name = serializers.CharField(required=False, allow_blank=True)
    jobCategory = serializers.CharField(source="job_category", required=False)
    lineManagement = serializers.PrimaryKeyRelatedField(
        source="line_management", queryset=User.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Job
        fields = [
            'id', 'name', 'description', 'department',
            'jobCategory', 'lineManagement',
            'responsibilities', 'line_management_full_name'
        ]

    def get_line_management_full_name(self, obj):
        if isinstance(obj, Job):
            return obj.get_line_management()
        return None
