from rest_framework import viewsets
from .serializers import CourseSerializer
from rest_framework.pagination import PageNumberPagination

from .models import Course


class CustomPagination(PageNumberPagination):
    page_size = 10


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
