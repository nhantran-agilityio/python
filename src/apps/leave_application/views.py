from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from django.http import HttpResponse
from io import BytesIO
from rest_framework import status
from reportlab.pdfgen import canvas
import csv
from rest_framework.parsers import MultiPartParser, FormParser
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from reportlab.lib.pagesizes import letter
import pandas as pd
from drf_yasg.utils import swagger_auto_schema
from apps.leave_application.models import (
    LeaveApplication,
    EmployeeLeaveBalance,
)
from apps.leave_application.serializers import (
    EmployeeLeaveBalanceSerializer,
    LeaveApplicationSerializer,
    LeaveApplicationStatusUpdateSerializer,
    RecallApplicationStatusUpdateSerializer,
    LeaveRecallSerializer
)


from rest_framework.permissions import BasePermission


class IsEmployee(BasePermission):
    """
    Custom permission to allow only admins or employees to access the view.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated and has the required role
        return (
            request.user.is_authenticated and
            request.user.role in ['candidate', 'employee']
        )


class IsAdmin(BasePermission):
    """
    Custom permission to allow only admins to access the view.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated and is an admin
        return request.user.is_authenticated and request.user.role == 'admin'


class LeaveApplicationPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 50
    page_size = 10

    def paginate_queryset(self, queryset, request, view=None):
        """
        Override paginate_queryset to handle invalid page numbers.
        """
        try:
            return super().paginate_queryset(queryset, request, view)
        except pagination.NotFound:
            # Return an empty list if the page does not exist
            self.page = None
            return []

    def get_paginated_response(self, data):
        """
        Return a paginated response with an empty array if the page is invalid.
        """
        if self.page is None:
            return Response({
                'count': 0,
                'next': None,
                'previous': None,
                'results': []
            })
        else:
            return Response({
                "metaData": {
                    "limit": self.page.paginator.per_page,
                    "page": self.page.number,
                    "totalCount": self.page.paginator.count
                },
                "results": data
            })
        return super().get_paginated_response(data)


class LeaveApplicationListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [CamelCaseJSONParser, MultiPartParser, FormParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_QUERY,
                              description="Filter by employee first name",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY,
                              description=(
                                  "Filter by type (comma-separated values, "
                                  "e.g., Annual,Sick)"
                              ),
                              type=openapi.TYPE_ARRAY,
                              items=openapi.Items(type=openapi.TYPE_STRING)
                              ),
            openapi.Parameter('isRecall', openapi.IN_QUERY,
                              description=(
                                  "Filter current active leaves "
                                  "(start_date <= today <= end_date)"
                              ),
                              type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('limit', openapi.IN_QUERY,
                              description="Number of results per page",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('page', openapi.IN_QUERY,
                              description="Page number",
                              type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = LeaveApplication.objects.all()
        first_name = request.query_params.get("first_name")
        leave_types = request.query_params.get("type")
        is_recall = request.query_params.get("isRecall", "false").lower() == "true"
        today = date.today()

        if first_name:
            queryset = queryset.filter(
                employee__first_name__icontains=first_name
            )

        if leave_types:
            leave_type_list = leave_types.split(',')
            queryset = queryset.filter(type__in=leave_type_list)

        if is_recall:
            queryset = queryset.filter(
                start_date__lte=today,
                end_date__gte=today,
                status="Approved"
            )

        paginator = LeaveApplicationPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = LeaveApplicationSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new leave application with an optional document upload.",
        request_body=LeaveApplicationSerializer,
        responses={
            201: "Leave application ion created successfully.",
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new leave application with file upload.
        """
        serializer = LeaveApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=request.user)  # Automatically set the employee
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveApplicationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [CamelCaseJSONParser, MultiPartParser, FormParser]

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
        """
        Retrieve the details of a specific leave application.
        """
        leave_application = get_object_or_404(LeaveApplication, pk=pk)
        serializer = LeaveApplicationSerializer(leave_application)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        """
        Partially update a leave application.
        """
        leave_application = get_object_or_404(LeaveApplication, pk=pk)
        serializer = LeaveApplicationSerializer(
            leave_application, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a leave application by its ID.",
        responses={
            204: "Leave application deleted successfully.",
            404: "Leave application not found."
        }
    )
    def delete(self, request, pk, *args, **kwargs):
        """
        Delete a leave application.
        """
        leave_application = get_object_or_404(LeaveApplication, pk=pk)
        leave_application.delete()
        return Response(
            {"message": "Leave application deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class LeaveApplicationDetailView(generics.RetrieveAPIView):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    permission_classes = [IsAuthenticated]


class LeaveApplicationByUserView(generics.ListAPIView):
    serializer_class = LeaveApplicationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LeaveApplicationPagination
    page_size_query_param = 'limit'
    max_page_size = 50

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return LeaveApplication.objects.filter(employee_id=user_id)


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


class LeaveApplicationDownloadView(APIView):
    def get(self, request, file_format, *args, **kwargs):
        """
        Download leave applications as PDF, CSV, or Excel file.

        Args:
            file_format (str): File format to download in.
                Choices are 'pdf', 'csv', 'excel'.

        Returns:
            HttpResponse: Response containing the downloaded file.
        """
        leave_applications = LeaveApplication.objects.select_related('employee').all()
        # Convert data to a list of dicts
        data = [
            {
                'employee': leave.employee.first_name,
                # Access the related employee's name
                'type': leave.type,
                'start_date': leave.start_date,
                'end_date': leave.end_date,
                'durations': leave.durations,
                'resumption_date': leave.resumption_date,
                'reason': leave.reason,
                'status': leave.status,
            }
            for leave in leave_applications
        ]

        if file_format == 'pdf':
            # Generate PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = (
                'attachment; filename="leave_applications.pdf"'
            )
            p = canvas.Canvas(response, pagesize=letter)
            p.drawString(100, 750, "Leave Applications")
            y_position = 730
            for application in data:
                p.drawString(
                    100, y_position,
                    f"Employee: {application['employee']} | "
                    f"Type: {application['type']} | "
                    f"start_date: {application['start_date']} | "
                    f"end_date: {application['end_date']} | "
                    f"reason: {application['reason']} | "
                    f"resumption_date: {application['resumption_date']} | "
                    f"durations: {application['durations']} | "
                    f"Status: {application['status']}"
                )
                y_position -= 20
            p.showPage()
            p.save()
            return response

        elif file_format == 'csv':
            # Generate CSV
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = (
                'attachment; filename="leave_applications.csv"'
            )
            fieldnames = ['employee', 'type', 'start_date', 'end_date',
                          'durations', 'resumption_date', 'reason', 'status']
            writer = csv.DictWriter(response, fieldnames=fieldnames)
            writer.writeheader()
            for application in data:
                writer.writerow({
                    'employee': application['employee'],
                    'type': application['type'],
                    'start_date': application['start_date'],
                    'end_date': application['end_date'],
                    'durations': application['durations'],
                    'resumption_date': application['resumption_date'],
                    'reason': application['reason'],
                    'status': application['status'],
                })
            return response

        elif file_format == 'excel':
            # Generate Excel
            response = HttpResponse(
                content_type=(
                    'application/vnd.openxmlformats-officedocument.'
                    'spreadsheetml.sheet'
                )
            )
            response['Content-Disposition'] = (
                'attachment; filename="leave_applications.xlsx"'
            )

            # Create Excel file using pandas and BytesIO
            fieldnames = ['employee', 'type', 'start_date', 'end_date',
                          'durations', 'resumption_date', 'reason', 'status']
            df = pd.DataFrame(data, columns=fieldnames)
            with BytesIO() as buffer:  # Use BytesIO for binary data
                with pd.ExcelWriter(
                    buffer, engine='openpyxl'
                ) as writer:
                    df.to_excel(
                        writer, index=False, sheet_name='Leave Applications'
                    )
                buffer.seek(0)
                response.write(buffer.getvalue())
            return response


class RecallLeaveApplicationView(APIView):
    permission_classes = [IsAuthenticated]

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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
