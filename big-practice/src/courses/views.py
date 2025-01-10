from rest_framework import viewsets
from .serializers import CourseSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from .models import Course
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        average_enrollments = Course.average_enrollments()
        top_courses = Course.top_courses()
        top_courses_data = CourseSerializer(top_courses, many=True).data
        return Response({
            'average_enrollments': average_enrollments,
            'top_courses': top_courses_data,
        })
