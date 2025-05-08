from leave_applications.export import (
    export_as_csv,
    export_as_excel,
    export_as_pdf,
)


def export_leave_applications(queryset, file_format):
    data = [{
        'employee': leave.employee.first_name,
        'type': leave.type,
        'start_date': leave.start_date,
        'end_date': leave.end_date,
        'durations': leave.durations,
        'resumption_date': leave.resumption_date,
        'reason': leave.reason,
        'status': leave.status,
    } for leave in queryset]

    if file_format == 'pdf':
        return export_as_pdf(data)
    elif file_format == 'csv':
        return export_as_csv(data)
    elif file_format == 'excel':
        return export_as_excel(data)
