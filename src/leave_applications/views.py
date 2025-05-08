from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from constants.base import SUPPORTED_FORMATS
from leave_applications.filter import LeaveApplicationFilter
from leave_applications.models import (
    LeaveApplication,
)
from leave_applications.serializers import (
    LeaveApplicationSerializer,
    LeaveRecallSerializer
    )
from leave_applications.services import LeaveApplicationExporter
from utils.custom_permissions import IsAdmin, IsEmployee
from core.responses import ApiResponse


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
        return ApiResponse(
            data=serializer.data,
            message="Leave applications retrieved successfully",
            status_code=status.HTTP_200_OK
        )


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
        return ApiResponse(
            data=serializer.data,
            message="Leave application recall updated successfully",
            status_code=status.HTTP_200_OK
        )


class LeaveApplicationDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_format):
        if file_format not in SUPPORTED_FORMATS:
            raise ValidationError(
                _(
                    f"Invalid format '{file_format}'. Allowed values are: "
                    f"{', '.join(SUPPORTED_FORMATS)}."
                )
            )

        user = request.user
        queryset = LeaveApplication.objects.select_related('employee')

        if IsEmployee().has_permission(request, self):
            queryset = queryset.filter(employee=user)

        if not queryset.exists():
            raise NotFound(_("No leave applications found."))

        exporter = LeaveApplicationExporter(queryset)
        return exporter.export(file_format)
