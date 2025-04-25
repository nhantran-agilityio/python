from rest_framework import serializers

from .models import LeaveApplication, EmployeeLeaveBalance


class LeaveRecallSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = [
            'recall_date',
            'recall_reason',
            'recall_status',
            'is_recalled'
        ]


class LeaveApplicationSerializer(serializers.ModelSerializer):
    relief_officer_first_name = serializers.SerializerMethodField()
    relief_officer_last_name = serializers.SerializerMethodField()
    employeeName = serializers.SerializerMethodField()

    class Meta:
        model = LeaveApplication
        fields = [
            "id",
            'start_date',
            'end_date',
            'resumption_date',
            'employeeName',
            'type',
            'relief_officer',
            'document_path',
            'reason',
            'durations',
            'relief_officer_first_name',
            'relief_officer_last_name',
            'status',
            'recall_status',
            'recall_reason',
            'recall_date',
            'is_recalled',
            'days_remaining',
            'created_at',
            'updated_at',
        ]

    def get_relief_officer_first_name(self, obj):
        if obj.relief_officer:
            return obj.relief_officer.first_name
        return None

    def get_relief_officer_last_name(self, obj):
        if obj.relief_officer:
            return obj.relief_officer.last_name
        return None

    def get_employeeName(self, obj):
        if obj.employee:
            return f"{obj.employee.first_name} {obj.employee.last_name}"
        return None

    def create(self, validated_data):
        validated_data['employee'] = self.context['request'].user
        return super().create(validated_data)


class EmployeeLeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeaveBalance
        fields = "__all__"


class LeaveApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = ['status']


class RecallApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = ['recall_status']
