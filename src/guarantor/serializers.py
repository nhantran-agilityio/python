from rest_framework import serializers

from guarantor.models import Guarantor


class GuarantorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantor
        exclude = ['user']
