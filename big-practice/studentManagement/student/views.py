from rest_framework import viewsets, permissions
from student.serializers import StudentSerializer
from rest_framework.pagination import PageNumberPagination
from .models import Student


class CustomPagination(PageNumberPagination):
    page_size = 10


class StudentViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    ordering_fields = ["first_name"]
    queryset = Student.objects.filter(is_active=True)
    serializer_class = StudentSerializer
