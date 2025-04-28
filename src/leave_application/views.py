from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from leave_application.models import (
    LeaveApplication,
    EmployeeLeaveBalance,
)
from leave_application.serializers import (
    EmployeeLeaveBalanceSerializer,
    LeaveApplicationSerializer,
    LeaveApplicationStatusUpdateSerializer,
    RecallApplicationStatusUpdateSerializer,
    LeaveRecallSerializer
)
from utils.conversions import parse_request_data, validate_and_respond
from utils.custom_permissions import IsAdmin, IsEmployee
from utils.export import export_as_csv, export_as_excel, export_as_pdf
from utils.filter import filter_leave_applications
from utils.pagination import CustomPagination


class LeaveApplicationListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self, request):
        user = request.user
        queryset = LeaveApplication.objects.select_related("employee")

        if IsEmployee():
            queryset = queryset.filter(employee=user)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("employeeName", openapi.IN_QUERY, description="Filter by employee name", type=openapi.TYPE_STRING),
            openapi.Parameter("type", openapi.IN_QUERY, description="Filter by leave type (comma-separated)", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
            openapi.Parameter("isRecall", openapi.IN_QUERY, description="Filter active recalls", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter("limit", openapi.IN_QUERY, description="Page size", type=openapi.TYPE_INTEGER),
            openapi.Parameter("page", openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)
        employee_name = request.query_params.get("employeeName")
        leave_types = request.query_params.get("type")
        is_recall = request.query_params.get("isRecall", "false").lower() == "true"
        filtered_qs = filter_leave_applications(
            queryset, employee_name, leave_types, is_recall
        )

        paginator = CustomPagination()
        paginated_qs = paginator.paginate_queryset(filtered_qs, request)
        serializer = LeaveApplicationSerializer(paginated_qs, many=True)

        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new leave application with file upload.",
        request_body=LeaveApplicationSerializer,
        responses={
            status.HTTP_201_CREATED: LeaveApplicationSerializer,
            status.HTTP_400_BAD_REQUEST: "Validation Error"
        }
    )
    def post(self, request, *args, **kwargs):
        data = parse_request_data(request.data)

        serializer, errors = validate_and_respond(
            LeaveApplicationSerializer,
            data=data,
            context={"request": request}
        )

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(employee=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LeaveApplicationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        return get_object_or_404(LeaveApplication, pk=pk)

    """
    API to retrieve the details of a specific leave application.
    """
    @swagger_auto_schema(
        operation_description="Retrieve the details of a specific leave application by its ID.",
        responses={
            200: openapi.Response(
                description="Leave application details retrieved successfully.",
                schema=LeaveApplicationSerializer
            ),
            404: "Leave application not found."
        }
    )
    def get(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        serializer = LeaveApplicationSerializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update an existing leave application",
        request_body=LeaveApplicationSerializer,
        responses={
            201: "Leave application updated successfully",
            400: "Bad Request",
            404: "Leave application not found."
        }
    )
    def patch(self, request, pk, *args, **kwargs):
        # Convert camelCase keys to snake_case
        data = parse_request_data(request.data)

        instance = self.get_object(pk)
        serializer, errors = validate_and_respond(
            LeaveApplicationSerializer, instance, data=data, partial=True
        )
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Delete a leave application by its ID.",
        responses={
            204: "Leave application deleted successfully.",
            404: "Leave application not found."
        }
    )
    def delete(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        instance.delete()
        return Response({"message": "Leave application deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)


class LeaveApplicationDetailView(generics.RetrieveAPIView):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    permission_classes = [IsAuthenticated]


class EmployeeLeaveBalanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeLeaveBalance.objects.all()
    serializer_class = EmployeeLeaveBalanceSerializer


class LeaveApplicationStatusUpdateView(generics.UpdateAPIView):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class RecallApplicationStatusUpdateView(generics.UpdateAPIView):
    queryset = LeaveApplication.objects.all()
    serializer_class = RecallApplicationStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsEmployee]


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
