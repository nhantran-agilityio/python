from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from leave_application.filter import LeaveApplicationFilter
from leave_application.models import (
    LeaveApplication,
)
from leave_application.serializers import (
    LeaveApplicationSerializer,
    LeaveRecallSerializer
    )
from utils.custom_permissions import IsAdmin, IsEmployee
from leave_application.export import (
    export_as_csv,
    export_as_excel,
    export_as_pdf,
)


class LeaveApplicationViewSet(viewsets.ModelViewSet):
    resource_name = "leave-applications"
    parser_classes = [MultiPartParser, FormParser]
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = LeaveApplicationFilter
    search_fields = ['employee__first_name', 'employee__last_name', 'type']

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = LeaveApplication.objects.select_related("employee")
        if IsEmployee():
            queryset = queryset.filter(employee=user)
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('type', openapi.IN_QUERY, description="Filter by leave type", type=openapi.TYPE_STRING),
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by status", type=openapi.TYPE_STRING),
            openapi.Parameter('employeeName', openapi.IN_QUERY, description="Filter by employee full name", type=openapi.TYPE_STRING),
            openapi.Parameter('isRecall', openapi.IN_QUERY, description="Filter active recalls", type=openapi.TYPE_BOOLEAN),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if self.paginator is not None:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecallLeaveApplicationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Update recall information of a leave application",
        request_body=LeaveRecallSerializer,
        responses={
            200: "Recall info updated successfully",
            400: "Invalid data",
            404: "LeaveApplication not found"
        }
    )
    def patch(self, request, pk):
        leave_application = get_object_or_404(LeaveApplication, pk=pk)

        serializer = LeaveRecallSerializer(leave_application, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LeaveApplicationDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_format):
        user = request.user
        queryset = LeaveApplication.objects.select_related('employee')
        if IsEmployee():
            queryset = queryset.filter(employee=user)

        data = [{
            'employee': leave.employee.first_name,
            'type': leave.type,
            'start_date': leave.start_date,
            'end_date': leave.end_date,
            'durations': leave.durations,
            'resumption_date': leave.resumption_date,
            'reason': leave.reason,
            'status': leave.status,
        } for leave in queryset]

        if not data:
            raise NotFound("No leave applications found")

        if file_format == 'pdf':
            return export_as_pdf(data)
        elif file_format == 'csv':
            return export_as_csv(data)
        elif file_format == 'excel':
            return export_as_excel(data)

        raise ValidationError("Invalid format. Allowed values are: pdf, csv, excel.")


apps = [LeaveApplicationViewSet]
