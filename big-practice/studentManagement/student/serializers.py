from rest_framework import serializers
from .models import Student
from courses.models import Course
from courses.serializers import CourseSerializer


class StudentSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='student-detail')
    courses = CourseSerializer(many=True)

    class Meta:
        model = Student
        fields = [
            # "url",
            "first_name",
            "last_name",
            "birthday",
            "gender",
            "email",
            "avatar",
            "address",
            "is_active",
            "courses",
        ]

    def create(self, validated_data):
        courses_data = validated_data.pop('courses')
        student = Student.objects.create(**validated_data)
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(**course_data)
            student.courses.remove(course)
        return student

    def update(self, instance, validated_data):
        courses_data = validated_data.pop('courses', [])
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.birthday = validated_data.get('birthday',
                                               instance.birthday)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.address = validated_data.get('address', instance.address)
        instance.is_active = validated_data.get('is_active',
                                                instance.is_active)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Clear existing courses and add new ones
        instance.courses.clear()
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(**course_data)
            instance.courses.add(course)

        return instance
