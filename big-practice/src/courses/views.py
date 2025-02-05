from rest_framework import viewsets
from .serializers import CourseSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
import logging
from .models import Course
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 10


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        logger.debug("Fetching course statistics")
        average_enrollments = Course.average_enrollments()
        logger.info(f"Average enrollments: {average_enrollments}")
        top_courses = Course.top_courses()
        logger.debug(f"Top courses: {top_courses}")
        top_courses_data = CourseSerializer(top_courses, many=True).data
        logger.debug("Returning response with course statistics")
        return Response({
            'average_enrollments': average_enrollments,
            'top_courses': top_courses_data,
        })
