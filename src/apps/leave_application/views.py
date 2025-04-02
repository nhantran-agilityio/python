from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
import csv
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
    LeaveApplicationStatusUpdateSerializer
)


class LeaveApplicationPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 50

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


class LeaveApplicationListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = LeaveApplication.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = LeaveApplicationSerializer
    pagination_class = LeaveApplicationPagination

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
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = LeaveApplication.objects.all()
        first_name = self.request.query_params.get("first_name", None)
        leave_types = self.request.query_params.get("type", None)

        if first_name:
            queryset = queryset.filter(
                employee__first_name__icontains=first_name)

        if leave_types:
            leave_type_list = leave_types.split(',')
            queryset = queryset.filter(type__in=leave_type_list)

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


class LeaveApplicationDownloadView(APIView):
    def get(self, request, file_format, *args, **kwargs):
        """
        Download leave applications as PDF, CSV, or Excel file.

        Args:
            file_format (str): File format to download in. Choices are 'pdf', 'csv', 'excel'.

        Returns:
            HttpResponse: Response containing the downloaded file.
        """
        leave_applications = LeaveApplication.objects.select_related('employee').all()
        # Convert data to a list of dicts
        data = [
            {
                'employee': leave.employee.first_name,  # Access the related employee's name
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
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
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
