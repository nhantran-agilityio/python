from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from contact.serializers import ContactSerializer
from job.serializers import JobSerializer
from kin.serializers import KinSerializer


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
    contact = ContactSerializer(required=False)
    kin = KinSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name',
            'avatar', 'role',
            'job', 'contact', 'phone',
            'is_receive_newsletters', 'email', 'kin'
        ]

    def update_or_create_nested(self, instance, nested_data, related_name, serializer_class):
        if not nested_data:
            return

        nested_instance = getattr(instance, related_name, None)

        if 'id' in nested_data:
            try:
                obj = serializer_class.Meta.model.objects.get(id=nested_data['id'])
                serializer = serializer_class(obj, data=nested_data, partial=True)
            except serializer_class.Meta.model.DoesNotExist:
                serializer = serializer_class(data=nested_data)
        elif nested_instance:
            serializer = serializer_class(nested_instance, data=nested_data, partial=True)
        else:
            serializer = serializer_class(data=nested_data)

        serializer.is_valid(raise_exception=True)
        saved = serializer.save()
        setattr(instance, related_name, saved)
        instance.save()

    def update(self, instance, validated_data):
        job_data = validated_data.pop('job', None)
        contact_data = validated_data.pop('contact', None)
        kin_data = validated_data.pop('kin', None)

        self.update_or_create_nested(instance, job_data, 'job', JobSerializer)
        self.update_or_create_nested(instance, contact_data, 'contact', ContactSerializer)
        self.update_or_create_nested(instance, kin_data, 'kin', KinSerializer)

        return super().update(instance, validated_data)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
