from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    phoneNum2 = serializers.CharField(source="phone_num_2", required=False)
    cityOfResidence = serializers.CharField(source="city_of_residence", required=False)
    residentialAddress = serializers.CharField(source="residential_address", required=False)

    class Meta:
        model = Contact
        fields = [
            "id",
            "phoneNum2",
            "cityOfResidence",
            "residentialAddress",
        ]
