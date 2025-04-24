
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.leave_application.models import LeaveApplication
from apps.accounts.models import User
from unittest.mock import Mock
from apps.leave_application.views import LeaveApplicationDownloadView


class LeaveApplicationListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.admin_user = User.objects.create_user('admin', 'admin@example.com', 'password', role='admin')
        self.client.force_authenticate(user=self.user)
        self.leave1 = LeaveApplication.objects.create(
            employee=self.user,
            type='Annual',
            start_date='2023-01-01',
            end_date='2023-01-10',
            durations=1,
            reason='Vacation',
            resumption_date='2023-01-11',
        )
        self.leave2 = LeaveApplication.objects.create(
            employee=self.user,
            type='Sick',
            start_date='2023-02-01',
            end_date='2023-02-10',
            durations=1,
            reason='Vacation',
            resumption_date='2023-01-11',
        )
        self.leave3 = LeaveApplication.objects.create(
            employee=self.admin_user,
            type='Annual',
            start_date='2023-03-01',
            end_date='2023-03-10',
            durations=1,
            resumption_date='2023-01-11',
            reason='Sick leave',
        )
        self.url = '/api/leave-applications/'

    def test_get_leave_applications(self):
        response = self.client.get(self.url, employee_name=self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_leave_application(self):
        data = {
            'type': 'Sick',
            'start_date': '2023-02-01',
            'end_date': '2023-02-10',
            'reason': 'Medical',
            'resumption_date': '2023-02-11',
            'durations': 1,
            'employee': self.user.id,
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LeaveApplication.objects.count(), 3)

    def test_create_leave_application_error(self):
        data = {
            'type': 'Sick',
            'start_date': '2023-02-01',
            'end_date': '2023-02-10',
            'reason': 'Medical',
            'resumption_date': '2023-02-11',
            'durations': 1,
            'employee': "123",
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(LeaveApplication.objects.count(), 4)


class TestRecallLeaveApplicationView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
        self.client.force_authenticate(user=self.user)
        self.leave_application = LeaveApplication.objects.create(
            employee=self.user,
            start_date='2023-02-01',
            end_date='2023-02-10',
            reason='Medical',
            resumption_date='2023-02-11',
            durations=1,
        )
        self.url = f'/api/leave-applications/{self.leave_application.pk}/recall/'

    def test_successful_update(self):
        data = {'recall_date': '2023-02-12', 'recall_reason': 'Test reason'}
        response = self.client.patch(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.leave_application.refresh_from_db()
        self.assertEqual(self.leave_application.recall_reason, 'Test reason')

    def test_update_with_invalid_data(self):
        data = {'recall_date': 'invalid-date'}
        response = self.client.patch(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('recall_date', response.data)

    def test_update_with_non_existent_leave_application(self):
        response = self.client.patch('/leave-applications/999/', {},
                                     format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestLeaveApplicationDownloadView(APITestCase):
    def setUp(self):
        self.view = LeaveApplicationDownloadView()
        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.request = Mock()
        self.request.user = self.user

        # Create leave applications for the user
        self.leave1 = LeaveApplication.objects.create(
            employee=self.user,
            type='Annual',
            start_date='2023-01-01',
            end_date='2023-01-10',
            durations=1,
            reason='Vacation',
            resumption_date='2023-01-11',
        )
        self.leave2 = LeaveApplication.objects.create(
            employee=self.user,
            type='Sick',
            start_date='2023-02-01',
            end_date='2023-02-10',
            durations=1,
            reason='Medical',
            resumption_date='2023-02-11',
        )

    def test_download_pdf(self):
        url = '/api/leave-applications/download/pdf/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_download_csv(self):
        url = '/api/leave-applications/download/csv/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_download_excel(self):
        url = '/api/leave-applications/download/excel/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_format(self):
        url = '/api/leave-applications/download/excels/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_found_when_no_data(self):
        self.leave1.delete()
        self.leave2.delete()
        url = '/api/leave-applications/download/excels/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertIn("No leave applications", str(response.data))


class LeaveApplicationDetailAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass1234')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.leave = LeaveApplication.objects.create(
            employee=self.user,
            type='Annual',
            start_date='2023-01-01',
            end_date='2023-01-10',
            durations=1,
            reason='Vacation',
            resumption_date='2023-01-11',
        )
        self.url = '/api/leave-applications/{}/'.format(self.leave.id)

    def test_get_leave_application_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type'], self.leave.type)

    def test_patch_leave_application(self):
        data = {
            "reason": "Updated reason"
        }
        response = self.client.patch(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.leave.refresh_from_db()
        self.assertEqual(self.leave.reason, "Updated reason")

    def test_delete_leave_application(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        leave_exists = LeaveApplication.objects.filter(
            pk=self.leave.pk
        ).exists()
        self.assertFalse(leave_exists)

    def test_get_leave_not_found(self):
        invalid_url = '/api/leave-applications/999/'
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_invalid_data(self):
        data = {
            "start_date": "invalid-date"
        }
        response = self.client.patch(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
