import unittest
from django.http import HttpResponse
from leave_application.api.export import export_as_csv, export_as_pdf, export_as_excel
from io import StringIO
import csv


class TestExportAsPdf(unittest.TestCase):
    def test_returns_http_response(self):
        data = [{'key': 'value'}]
        response = export_as_pdf(data)
        self.assertIsInstance(response, HttpResponse)

    def test_content_type(self):
        data = [{'key': 'value'}]
        response = export_as_pdf(data)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_content_disposition(self):
        data = [{'key': 'value'}]
        response = export_as_pdf(data)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="leave_applications.pdf"')


class TestExportAsCSV(unittest.TestCase):

    def test_valid_data(self):
        data = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}]
        response = export_as_csv(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="leave_applications.csv"')
        csv_reader = csv.DictReader(StringIO(response.content.decode('utf-8')))
        rows = list(csv_reader)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['name'], 'John')
        self.assertEqual(rows[0]['age'], '30')
        self.assertEqual(rows[1]['name'], 'Jane')
        self.assertEqual(rows[1]['age'], '25')


class TestExportAsExcel(unittest.TestCase):

    def test_export_as_excel_valid_data(self):
        data = [{'Name': 'John', 'Age': 30}, {'Name': 'Alice', 'Age': 25}]
        response = export_as_excel(data)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="leave_applications.xlsx"')
        self.assertGreater(len(response.content), 0)

    def test_export_as_excel_empty_data(self):
        data = []
        response = export_as_excel(data)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="leave_applications.xlsx"')
        self.assertGreater(len(response.content), 0)
