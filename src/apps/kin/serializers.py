from rest_framework import serializers

from .models import Kin


class KinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kin
        fields = '__all__'
