from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import (
    CharField,
    EmailField,
    ValidationError,
)
from django.contrib.auth import authenticate

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user register with password and confirm_password validate.
    """
    username = CharField(validators=[UniqueValidator(
        queryset=User.objects.all())])
    email = EmailField(validators=[UniqueValidator(
        queryset=User.objects.all())])
    firstName = CharField(source="first_name", allow_blank=True,
                          required=False)
    lastName = CharField(source="last_name", allow_blank=True,
                         required=False)
    password = CharField(write_only=True, min_length=8,
                         validators=[validate_password])
    confirmPassword = CharField(write_only=True, source="confirm_password")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "confirmPassword",
            "lastName",
            "firstName"
        )

    def validate(self, attrs: dict):
        if attrs["password"] != attrs["confirm_password"]:
            raise ValidationError(
                {"confirm_password": "Password field didn't match."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        user = authenticate(username=data['username'],
                            password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return data
