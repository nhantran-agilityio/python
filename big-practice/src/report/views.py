from rest_framework import viewsets
from django.shortcuts import render
from .serializers import ReportSerializer
from rest_framework.pagination import PageNumberPagination
from .models import Report


class CustomPagination(PageNumberPagination):
    page_size = 10


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().select_related('student', 'course')
    serializer_class = ReportSerializer
    pagination_class = CustomPagination


def report_list(request):
    reports = Report.objects.all().select_related('student', 'course')
    return render(request, 'report_list.html', {'reports': reports})
