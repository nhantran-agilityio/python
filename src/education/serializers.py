from rest_framework import serializers

from .models import Education


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ['user']
