from rest_framework import serializers

from .models import Kin


class KinSerializer(serializers.ModelSerializer):
    residentialAddress = serializers.CharField(
        source="residential_address", required=False
    )

    class Meta:
        model = Kin
        fields = [
            "id",
            "name",
            "job",
            "phone",
            "relationship",
            "residentialAddress",
        ]
