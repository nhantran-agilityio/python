
from accounts.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class JobResponsibilityListCreateViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            username="testuser",
            first_name="Test",
            last_name="User"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = "/api/job-responsibilities/"

    def test_list_job_responsibilities(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
