
from apps.job_responsibility.models import JobResponsibility
from rest_framework.test import APITestCase
from rest_framework import status


class JobResponsibilityListCreateViewTests(APITestCase):
    def setUp(self):
        self.url = "/api/job-responsibilities/"

    def test_list_job_responsibilities(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_job_responsibility(self):
        data = {'job': '12', 'description': 'New Responsibility'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobResponsibility.objects.count(), 1)
        self.assertEqual(JobResponsibility.objects.get().description, 'New Responsibility')
