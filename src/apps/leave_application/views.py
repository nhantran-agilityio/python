from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from rest_framework.response import Response
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
    page_size = 5  # Number of records per page
    page_size_query_param = 'page_size'
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
