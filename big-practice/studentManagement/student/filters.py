import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Student


class StudentFilter(django_filters.FilterSet):
    full_name = filters.CharFilter(method="filter_by_name")
    first_name = django_filters.CharFilter(lookup_expr='icontains',
                                           label='First Name')
    last_name = django_filters.CharFilter(lookup_expr='icontains',
                                          label='Last Name')
    email = django_filters.CharFilter(lookup_expr='icontains', label='Email')
    birth_date_from = django_filters.DateFilter(field_name='birthday',
                                                lookup_expr='gte',
                                                label='Birth Date From')
    birth_date_to = django_filters.DateFilter(field_name='birthday',
                                              lookup_expr='lte',
                                              label='Birth Date To')
    course_id = filters.CharFilter(field_name='courses__id',
                                   lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['full_name', 'course_id', 'first_name', 'last_name', 'email',
                  'birth_date_from', 'birth_date_to']

    def filter_by_name(self, queryset, _, value):
        """
        Custom query to filter student by first name, last name, or full name.
        """
        names = value.split()
        if len(names) == 2:
            first_name, last_name = names
            return queryset.filter(Q(first_name__icontains=first_name,
                                     last_name__icontains=last_name))
        else:
            return queryset.filter(Q(first_name__icontains=value) |
                                   Q(last_name__icontains=value))
