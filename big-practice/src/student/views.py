from rest_framework import viewsets
from student.serializers import StudentSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student
from .filters import StudentFilter
from django.shortcuts import render


class CustomPagination(PageNumberPagination):
    page_size = 10


class StudentViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = Student.objects.filter(is_active=True)\
        .select_related('user')\
        .order_by("first_name")
    serializer_class = StudentSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = StudentFilter


def home(request):
    return render(request, 'home.html')
