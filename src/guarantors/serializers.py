from rest_framework import serializers

from guarantors.models import Guarantor


class GuarantorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantor
        exclude = ['user']
