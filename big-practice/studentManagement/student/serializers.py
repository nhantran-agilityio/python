from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='student-detail')

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
            "is_active"
        ]
