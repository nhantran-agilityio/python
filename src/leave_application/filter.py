# filters.py
import django_filters
from datetime import date
from django.db.models.functions import Concat, Lower, Replace
from django.db.models import Value
from leave_application.models import LeaveApplication


class LeaveApplicationFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(method='filter_by_full_name', label='Employee Full Name')
    isRecall = django_filters.BooleanFilter(field_name='is_recalled')

    class Meta:
        model = LeaveApplication
        fields = ['type', 'status', 'isRecall']

    def filter_leave_applications(
        queryset, employee_name=None, leave_types=None, is_recall=False
    ):
        today = date.today()

        if employee_name:
            search_name = employee_name.replace(" ", "").lower()
            queryset = queryset.annotate(
                full_name_normalized=Lower(
                    Replace(
                        Concat(
                            'employee__first_name',
                            Value(''),
                            'employee__last_name'
                        ),
                        Value(" "),
                        Value("")
                    )
                )
            ).filter(full_name_normalized__icontains=search_name)

        if leave_types:
            leave_type_list = leave_types.split(',')
            queryset = queryset.filter(type__in=leave_type_list)

        if is_recall:
            queryset = queryset.filter(
                start_date__lte=today,
                end_date__gte=today,
                status="Approved"
            )

        return queryset
