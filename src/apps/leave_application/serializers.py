from rest_framework import serializers
from .models import LeaveApplication, EmployeeLeaveBalance


class LeaveApplicationSerializer(serializers.ModelSerializer):
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
