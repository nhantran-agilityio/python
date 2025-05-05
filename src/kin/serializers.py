from rest_framework import serializers

from kin.models import Kin


class KinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kin
        fields = '__all__'
