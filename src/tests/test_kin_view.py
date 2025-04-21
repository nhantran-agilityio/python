from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.accounts.models import User
from apps.kin.models import Kin


class KinViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            username="testuser"
        )

        self.client.login(username="testuser", password="testpass")
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='strongpass123',
            username='testuser'
        )
        self.kin = Kin.objects.create(
            name="Jane Doe",
            job="Software Engineer",
            phone="0987654321",
            relationship="Sister",
            residential_address="123 Main Street, District 1, Ho Chi Minh City"
        )
        self.user.kin = self.kin
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_kin_success(self):
        url = "/api/kins/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Success')
        self.assertEqual(response.data['data']['id'], str(self.kin.id))
        self.assertEqual(response.data['data']['name'], 'John Doe')

    def test_retrieve_kin_not_found(self):
        url = "/api/kins/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'No Kin found with the given ID.')
        self.assertIsNone(response.data['data'])
