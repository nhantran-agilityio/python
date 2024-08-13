from rest_framework import viewsets
from .serializers import ReportSerializer
from rest_framework.pagination import PageNumberPagination

from .models import Report


class CustomPagination(PageNumberPagination):
    page_size = 10


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    pagination_class = CustomPagination
