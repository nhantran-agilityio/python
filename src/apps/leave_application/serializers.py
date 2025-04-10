from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import LeaveApplication, EmployeeLeaveBalance


class ReliefOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name", "email"]


class LeaveApplicationSerializer(serializers.ModelSerializer):
    relief_officer = ReliefOfficerSerializer(read_only=True)
    employee_name = serializers.CharField(source="employee.first_name",
                                          read_only=True)

    class Meta:
        model = LeaveApplication
        fields = "__all__"


class EmployeeLeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeaveBalance
        fields = "__all__"


class LeaveApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = ['status']
