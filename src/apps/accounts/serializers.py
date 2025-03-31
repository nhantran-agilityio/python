# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from apps.document.models import Document
from apps.document.seralizers import DocumentSerializer
from apps.job.seralizers import JobSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    documents = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'job', 'documents', 'phone',
            'password', 'confirm_password', 'role', 'is_receive_newsletters', 'avatar'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        documents_data = validated_data.pop('documents', None)
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])

        user = User.objects.create(**validated_data)

        if documents_data:
            for document_data in documents_data:
                Document.objects.create(user=user, document_file=document_data)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'job', 'documents', 'phone', 'avatar', 'created_at',
            'updated_at', 'role', 'is_receive_newsletters', 'is_active'
        ]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
