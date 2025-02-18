from django.contrib import admin
from .models import Course
from notifications.models import Notification
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    search_fields = (
        'student__first_name',
        'student__last_name',
        'course__name'
    )
    list_filter = ('course', 'enrolled_at')

    def delete_model(self, request, obj):
        student = obj.student
        course = obj.course
        message = f'You have been removed from the course: {course.name}.'
        Notification.objects.create(user=student.user, message=message)
        super().delete_model(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filter by course if course_id is passed in the URL
        course_id = request.GET.get('course')
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "duration",
        "updated_at",
        "is_introductory",
        "enrollment_limit",
        "display_instructors",
        "is_active"
    )

    def display_instructors(self, obj):
        instructors = [instructor.name for instructor in obj.instructors.all()]
        return ", ".join(instructors)
    display_instructors.short_description = 'Instructors'

    def get_queryset(self, request):
        # Optionally, add a filter by course to the Student admin
        qs = super().get_queryset(request)
        # Filter by course if course_id is passed in the URL
        course_id = request.GET.get('course')
        if course_id:
            qs = qs.filter(enrollments__course_id=course_id)
        return qs

    def delete_model(self, request, obj):
        # Notify students before deleting the course
        enrollments = Enrollment.objects.filter(course=obj)
        for enrollment in enrollments:
            student = enrollment.student
            message = f'You have been removed from the course: {obj.name}.'
            Notification.objects.create(user=student.user, message=message)
        super().delete_model(request, obj)


# Register your models here.
admin.site.register(Course, CourseAdmin)
