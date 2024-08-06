from rest_framework import serializers
from .models import Student
from courses.serializers import CourseSerializer
from report.serializers import ReportSerializer


class StudentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='student-detail')
    courses = CourseSerializer(many=True)
    report = ReportSerializer()

    class Meta:
        model = Student
        fields = [
            "url",
            "first_name",
            "last_name",
            "birthday",
            "gender",
            "email",
            "avatar",
            "address",
            "is_active",
            "courses",
            "report"
        ]
