from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "name",
            "description",
            "duration",
            "thumbnail",
            "is_introductory",
            "enrollment_limit",
            "instructors",
            "is_active"
        ]
