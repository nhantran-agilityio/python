from django.contrib import admin
from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'duration')

    # Optionally, add a filter by course to the Student admin
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filter by course if course_id is passed in the URL
        course_id = request.GET.get('course')
        if course_id:
            qs = qs.filter(enrollments__course_id=course_id)
        return qs


# Register your models here.
admin.site.register(Course, CourseAdmin)
