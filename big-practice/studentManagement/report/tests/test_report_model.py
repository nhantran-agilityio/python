from django.test import TestCase
from datetime import timedelta
from report.models import Report
from student.models import Student
from courses.models import Course


class ReportModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            is_active=True,
            address="123 Main St",
            email="john.doe@example.com",
            gender="Male",
            birthday='1990-01-01',
        )

        self.course = Course.objects.create(
            name='React',
            duration=timedelta(days=1, hours=5),
            description="This is react course",
        )

        self.report = Report.objects.create(
            point='10',
            description='description',
            student=self.student,
            course=self.course,
        )

    def test_Report_Student(self):
        report = Report.objects.first()
        self.assertEqual(report.student.first_name, "John")

    def test_str_method(self):
        point = Report.objects.get(point="10")
        self.assertEqual(str(point), "John Doe - React - 10")

    def test_description_max_length(self):
        report = Report.objects.first()
        max_length = report._meta.get_field("description").max_length
        self.assertEqual(max_length, 150)

    def test_description_null_or_blank(self):
        report = Report.objects.first()
        self.assertTrue(report.description, None)
