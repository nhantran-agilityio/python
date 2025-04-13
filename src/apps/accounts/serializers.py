from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from apps.job.models import Job
from apps.job.seralizers import JobSerializer


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone', 'password', 'confirm_password', 'role',
            'is_receive_newsletters', 'avatar'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])

        user = User.objects.create(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    job_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name',
            'role', 'avatar',
            'job', 'job_id'
        ]

    def update(self, instance, validated_data):
        job_data = validated_data.pop("job", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if job_data:
            if instance.job:
                # update job existing
                for attr, value in job_data.items():
                    setattr(instance.job, attr, value)
                instance.job.save()
            else:
                # Create a new job if it doesn't exist
                new_job = Job.objects.create(**job_data)
                instance.job = new_job

        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
