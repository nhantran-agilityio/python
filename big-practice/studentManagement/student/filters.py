import django_filters
from django_filters import rest_framework as filters
from .models import Student


class StudentFilter(django_filters.FilterSet):
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
        fields = ['course_id', 'first_name', 'last_name', 'email',
                  'birth_date_from', 'birth_date_to']
