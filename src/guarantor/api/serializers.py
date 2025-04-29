from rest_framework import serializers

from ..models import Guarantor


class GuarantorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantor
        exclude = ['user']
