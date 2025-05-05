import csv
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def export_as_pdf(data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="leave_applications.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Leave Applications")
    y_position = 730
    for application in data:
        p.drawString(100, y_position, ' | '.join(f"{k.title().replace('_', ' ')}: {v}" for k, v in application.items()))
        y_position -= 20
    p.showPage()
    p.save()
    return response


def export_as_csv(data):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="leave_applications.csv"'
    writer = csv.DictWriter(response, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return response


def export_as_excel(data):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="leave_applications.xlsx"'
    df = pd.DataFrame(data)
    with BytesIO() as buffer:
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Leave Applications')
        buffer.seek(0)
        response.write(buffer.getvalue())
    return response
