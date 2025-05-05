from rest_framework import serializers

from educations.models import Education


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ['user']
