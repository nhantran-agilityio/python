from rest_framework import serializers
from .models import LeaveApplication, EmployeeLeaveBalance


class LeaveApplicationSerializer(serializers.ModelSerializer):
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')
    resumptionDate = serializers.DateField(source='resumption_date')
    employee_name = serializers.CharField(source="employee.first_name",
                                          read_only=True)

    relief_officer_id = serializers.UUIDField(write_only=True, required=False,
                                              allow_null=True)
    relief_officer_first_name = serializers.SerializerMethodField()
    relief_officer_last_name = serializers.SerializerMethodField()

    class Meta:
        model = LeaveApplication
        fields = [
            "id",
            'startDate',
            'endDate',
            'resumptionDate',
            'type',
            'employee',
            'relief_officer',
            'document_path',
            'reason',
            'durations',
            'relief_officer_id',
            'employee_name',
            'relief_officer_first_name',
            'relief_officer_last_name',
            'status',
            'recall_status',
            'new_resumption_date',
            'recall_reason',
            'recall_date',
            'is_recalled',
            'resumption_date',
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
