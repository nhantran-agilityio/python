from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import APIClient
from datetime import timedelta

from report.models import Report
from student.models import Student
from courses.models import Course


class ReportViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.report1 = Report.objects.create(point='10',
                                             description='description',
                                             )
        self.report2 = Report.objects.create(point='20',
                                             description='description',
                                             )

    def test_get_report_list(self):
        response = self.client.get('/reports/?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_report_detail(self):
        response = self.client.get(f'/reports/{self.report1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['point'], 10)

    def test_delete_report(self):
        response = self.client.delete(f'/reports/{self.report1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Report.objects.count(), 1)

    def test_create_report_valid_data(self):
        student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            is_active=True,
            address="123 Main St",
            email="john.doe@example.com",
            gender="Male",
            birthday='1990-01-01',
        )

        course = Course.objects.create(
            name='React',
            duration=timedelta(days=1, hours=5),
            description="This is react course",
        )
        data = {
            'point': '10',
            'description': 'Test report',
            'student': student.pk,  # Use the student's ID
            'course': course.pk  # Use the course's ID
        }
        response = self.client.post('/reports/', data, format='json')
        print("response.status_code", response.status_code)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_report(self):
        student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            is_active=True,
            address="123 Main St",
            email="john.doe@example.com",
            gender="Male",
            birthday='1990-01-01',
        )

        course = Course.objects.create(
            name='React',
            duration=timedelta(days=1, hours=5),
            description="This is react course",
        )
        data = {'point': '40', 'description': 'updated description',
                'student': student.pk,
                'course': course.pk}
        response = self.client.put(f'/reports/{self.report1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Report.objects.get(id=self.report1.id).point, 40)
