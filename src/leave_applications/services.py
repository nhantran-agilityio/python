from leave_applications.export import (
    export_as_csv,
    export_as_excel,
    export_as_pdf,
)


class LeaveApplicationExporter:
    def __init__(self, queryset):
        self.data = [{
            'user': leave.user.first_name,
            'type': leave.type,
            'start_date': leave.start_date,
            'end_date': leave.end_date,
            'durations': leave.durations,
            'resumption_date': leave.resumption_date,
            'reason': leave.reason,
            'status': leave.status,
        } for leave in queryset]

    def export(self, file_format):
        if file_format == 'pdf':
            return export_as_pdf(self.data)
        elif file_format == 'csv':
            return export_as_csv(self.data)
        elif file_format == 'excel':
            return export_as_excel(self.data)
        raise ValueError(f"Unsupported format: {file_format}")
