from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.views import View
from .models import Course, Enrollment
from student.models import Student
from .serializers import CourseSerializer
from rest_framework.pagination import PageNumberPagination
import logging
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class CustomPagination(PageNumberPagination):
    page_size = 10


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(CACHE_TTL))
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

    @action(detail=False, methods=['post'])
    def enroll(self, request):
        """
        Enroll a student in a course
        """
        course_id = request.data.get('course_id')
        student_id = request.data.get('student_id')

        try:
            course = Course.objects.get(id=course_id)
            student = Student.objects.get(id=student_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=404)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

        enrollment = Enrollment.objects.create(
            course=course, student=student)
        return Response({
            'status': 'enrolled',
            'enrollment_id': enrollment.id
        })


class CourseStatisticsView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        average_enrollments = Course.average_enrollments()
        top_courses = Course.top_courses().select_related('instructor').prefetch_related('enrollments__student')
        return render(request, 'statistics.html', {
            'average_enrollments': average_enrollments,
            'top_courses': top_courses,
        })


def course_list(request):
    courses = Course.objects.prefetch_related('instructors').all()
    return render(request, 'course_list.html', {'courses': courses})
