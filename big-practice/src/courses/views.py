from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Enrollment
from student.models import Student
from .serializers import CourseSerializer
from rest_framework.pagination import PageNumberPagination
import logging

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

    @action(detail=False, methods=['post'])
    def enroll(self, request):
        course_id = request.data.get('course_id')
        student_id = request.data.get('student_id')

        try:
            course = Course.objects.get(id=course_id)
            student = Student.objects.get(id=student_id)
            enrollment = Enrollment.objects.create(
                course=course, student=student)
            return Response({
                'status': 'enrolled',
                'enrollment_id': enrollment.id
            })
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=404)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
