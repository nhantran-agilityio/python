from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
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
from core.api_views import BaseAuthenticatedModelViewSet
from core.pagination import CustomPagination
from leave_applications.filter import LeaveApplicationFilter
from leave_applications.models import (
    LeaveApplication,
)
from leave_applications.serializers import (
    LeaveApplicationSerializer,
    LeaveRecallSerializer
    )
from leave_applications.services import LeaveApplicationExporter
from core.custom_permissions import IsAdmin, IsAdminOrOwner, IsEmployee
from core.responses import ApiResponse


class LeaveApplicationViewSet(BaseAuthenticatedModelViewSet):
    permission_classes = [IsAdminOrOwner]
    resource_name = "leave-applications"
    parser_classes = [MultiPartParser, FormParser]
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = LeaveApplicationFilter
    search_fields = ['employee__first_name', 'employee__last_name', 'type']
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """
        Saves the leave application to the database, with the current user as the employee
        """
        serializer.save(employee=self.request.user)

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated(), IsAdminOrOwner()]
        elif self.action == 'retrieve':
            return [IsAuthenticated(), IsEmployee()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrOwner()]
        elif self.action == 'create':
            return [IsAuthenticated(), IsEmployee()]
        return [AllowAny()]

    def get_queryset(self):
        """
        Returns a queryset of leave applications for the requesting user.

        If the user is an admin, this queryset will contain all leave applications.
        If the user is not an admin, this queryset will contain only the leave
        applications associated with the requesting user.
        """
        return LeaveApplication.objects.select_related("employee").for_user(
            self.request.user
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("employeeName", openapi.IN_QUERY, description="Filter by employee name", type=openapi.TYPE_STRING),
            openapi.Parameter("type", openapi.IN_QUERY, description="Filter by leave type (comma-separated)", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
            openapi.Parameter("isRecall", openapi.IN_QUERY, description="Filter active recalls", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter("limit", openapi.IN_QUERY, description="Page size", type=openapi.TYPE_INTEGER),
            openapi.Parameter("page", openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all leave applications.

        Parameters:
        - type: str (optional) - Filter by leave type
        - status: str (optional) - Filter by status
        - employeeName: str (optional) - Filter by employee full name
        - isRecall: bool (optional) - Filter active recalls

        Returns:
        - ApiResponse: A paginated list of leave applications
        """
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
        operation_description=(
            "Update recall information of a leave application"
        ),
        request_body=LeaveRecallSerializer,
        responses={
            200: "Recall info updated successfully",
            400: "Invalid data",
            404: "LeaveApplication not found"
        }
    )
    def patch(self, request, pk):
        """
        Partially updates the recall information of a specific leave application.

        Retrieves the leave application by primary key (pk) and updates its recall
        information using data provided in the request body. The update is partial,
        meaning only the fields included in the request will be updated.

        Parameters:
        - request (Request): The HTTP request object containing the update data.
        - pk (str): The primary key of the leave application to update.

        Returns:
        - ApiResponse: Contains the updated leave application data and a success message.

        Raises:
        - ValidationError: If the provided data is invalid.
        - NotFound: If the leave application with the given pk does not exist.
        """

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
        """
        Retrieves leave applications and exports them in the specified format.

        This method gets the leave applications for the authenticated user and exports
        them in the format specified by `file_format`. If the user is an employee, only
        their leave applications are included. If no leave applications are found, a
        `NotFound` exception is raised. Only formats listed in `SUPPORTED_FORMATS` are
        allowed; otherwise, a `ValidationError` is raised.

        Parameters:
        - request (Request): The HTTP request object containing user information.
        - file_format (str): The format in which to export the leave applications.

        Returns:
        - HttpResponse: The exported leave applications in the desired format.

        Raises:
        - ValidationError: If the `file_format` is not supported.
        - NotFound: If no leave applications are found for the user.
        """

        if file_format not in SUPPORTED_FORMATS:
            raise ValidationError(
                _(
                    f"Invalid format '{file_format}'. Allowed values are: "
                    f"{', '.join(SUPPORTED_FORMATS)}."
                )
            )

        queryset = LeaveApplication.objects.select_related(
            "employee"
        ).for_user(self.request.user)

        if not queryset.exists():
            raise NotFound(_("No leave applications found."))

        exporter = LeaveApplicationExporter(queryset)
        return exporter.export(file_format)
