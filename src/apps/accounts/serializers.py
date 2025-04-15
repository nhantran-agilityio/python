from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from apps.contact.models import Contact
from apps.contact.serializers import ContactSerializer
from apps.job.models import Job
from apps.job.seralizers import JobSerializer
from apps.kin.models import Kin
from apps.kin.serializers import KinSerializer


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
    job = JobSerializer(required=False)
    job_id = serializers.UUIDField(write_only=True, required=False)
    contact_id = serializers.UUIDField(write_only=True, required=False)
    contact = ContactSerializer(required=False)
    kin = KinSerializer(required=False)
    kin_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name',
            'role', 'avatar',
            'job', 'job_id', 'contact', 'phone',
            'is_receive_newsletters', 'email', 'contact_id', 'kin', 'kin_id'
        ]

    def update_or_create_nested(self, instance, nested_data, related_name, serializer_class):
        if nested_data:
            nested_instance = getattr(instance, related_name)
            if nested_instance:
                serializer = serializer_class(nested_instance, data=nested_data)
            else:
                serializer = serializer_class(data=nested_data)
            serializer.is_valid(raise_exception=True)
            saved = serializer.save()
            setattr(instance, related_name, saved)

    def update(self, instance, validated_data):
        job_data = validated_data.pop('job', None)
        contact_data = validated_data.pop('contact', None)
        kin_data = validated_data.pop('kin', None)

        self.update_or_create_nested(instance, job_data, 'job', JobSerializer)
        self.update_or_create_nested(instance, contact_data, 'contact', ContactSerializer)
        self.update_or_create_nested(instance, kin_data, 'kin', KinSerializer)

        return super().update(instance, validated_data)

    # def update(self, instance, validated_data):
    #     """Update a user and its related objects."""
    #     for field, value in validated_data.items():
    #         if field == 'job':
    #             if instance.job:
    #                 Job.objects.filter(id=instance.job.id).update(**value)
    #             else:
    #                 job = Job.objects.create(**value)
    #                 instance.job = job
    #         elif field == 'contact':
    #             if instance.contact:
    #                 Contact.objects.filter(id=instance.contact.id).update(**value)
    #             else:
    #                 contact = Contact.objects.create(**value)
    #                 instance.contact = contact
    #         elif field == 'kin':
    #             if instance.kin:
    #                 Kin.objects.filter(id=instance.kin.id).update(**value)
    #             else:
    #                 kin = Kin.objects.create(**value)
    #                 instance.kin = kin
    #         else:
    #             setattr(instance, field, value)

    #     instance.save()
    #     return instance


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
