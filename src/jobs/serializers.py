from rest_framework import serializers

from jobs.models import Job


class JobSerializer(serializers.ModelSerializer):
    responsibilities = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )
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
