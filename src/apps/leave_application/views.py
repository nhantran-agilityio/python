from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.leave_application.models import (
    LeaveApplication,
    EmployeeLeaveBalance,
)
from apps.leave_application.serializers import (
    EmployeeLeaveBalanceSerializer,
    LeaveApplicationSerializer,
    LeaveApplicationStatusUpdateSerializer
)


class LeaveApplicationListView(generics.ListCreateAPIView):
    queryset = LeaveApplication.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = LeaveApplicationSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_QUERY,
                              description="Filter by employee first name",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY,
                              description="Filter by type",
                              type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = LeaveApplication.objects.all()
        first_name = self.request.query_params.get("first_name", None)
        leave_type = self.request.query_params.get("type", None)

        if first_name:
            queryset = queryset.filter(
                employee__first_name__icontains=first_name)

        if leave_type:
            queryset = queryset.filter(type__iexact=leave_type)

        return queryset


class LeaveApplicationDetailView(generics.RetrieveAPIView):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    permission_classes = [IsAuthenticated]


class LeaveApplicationByUserView(generics.ListAPIView):
    serializer_class = LeaveApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return LeaveApplication.objects.filter(employee_id=user_id)


class EmployeeLeaveBalanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeLeaveBalance.objects.all()
    serializer_class = EmployeeLeaveBalanceSerializer


class LeaveApplicationStatusUpdateView(generics.UpdateAPIView):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationStatusUpdateSerializer
    permission_classes = [IsAuthenticated]
