from django.contrib import admin
from .models import Student
from courses.models import Course


class CourseListFilter(admin.SimpleListFilter):
    title = 'course'
    parameter_name = 'course'

    def lookups(self, request, model_admin):
        courses = Course.objects.all()
        return [(course.id, course.name) for course in courses]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(courses__id=self.value())
        return queryset


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "birthday",
        "gender",
        "email",
        "avatar",
        "address",
        "is_active",
    )
    search_fields = ("first_name", "last_name", "email")
    list_filter = (CourseListFilter,)


admin.site.register(Student, StudentAdmin)
