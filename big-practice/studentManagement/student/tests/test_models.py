from django.test import TestCase
from datetime import date
from student.models import Student
from courses.models import Course
from report.models import Report


class StudentModelTest(TestCase):
    def setUp(self):
        # Create a test Course
        self.course = Course.objects.create(
            name="Python",
            description="This is python course",
            duration="3 months"
        )

        # Create a test Report
        self.report = Report.objects.create(
            point=10,
            description="Good",
            student="Nhan",
            course="Python"
        )

        self.student = Student.objects.create(
            first_name='Nhan',
            last_name='Tran',
            is_Active=True,
            address="80 Le Cao Lang",
            email="test@gmail.com",
            gender="Male",
            birthday=date(1990, 6, 15),
            course=self.course,
            report=self.report,
        )

    def test_full_name(self):
        self.assertEqual(self.student.full_name, 'Nhansd Trana')

