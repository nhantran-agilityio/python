from rest_framework import serializers

from families.models import Family


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        exclude = ['user']
