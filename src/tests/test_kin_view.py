from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.kin.models import Kin
User = get_user_model()


class KinDetailAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            username="testuser"
        )

        self.client.login(username="testuser", password="testpass")
        self.kin = Kin.objects.create(
            name="Jane Doe",
            job="Software Engineer",
            phone="0987654321",
            relationship="Sister",
            residential_address="123 Main Street, District 1, Ho Chi Minh City"
        )
        self.user.kin = self.kin
        self.user.save()

        self.user_without_kin = User.objects.create_user(
            email='nocon@example.com',
            password='testpassword',
            first_name='No',
            username='no_kin',
            last_name='kin'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_kin_detail_success(self):
        url = "/api/kins/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_kin_detail_not_found(self):
        self.client.force_authenticate(user=self.user_without_kin)
        url = "/api/kins/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_kin_not_found(self):
        self.client.force_authenticate(user=self.user_without_kin)
        url = "/api/kins/"
        data = {
            "phone": "0123456789"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_kin_success(self):
        self.client.force_authenticate(user=self.user_without_kin)
        url = "/api/kins/"
        data = {
            "name": "Jone Doe",
            "job": "Software Engineer",
            "phone": "0987654321",
            "relationship": "Sister",
            "residential_address": "123 Main Street, District 1, Ho Chi Minh City"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


def test_post_kin_invalid_data(self):
    self.client.force_authenticate(user=self.user_without_kin)
    url = "/api/kins/"
    data = {
        "phone": "0123456789",
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('cityOfResidence', response.data)
    self.assertIn('residentialAddress', response.data)


def test_post_kin_when_already_exists(self):
    self.client.force_authenticate(user=self.user_with_kin)
    url = "/api/kins/"

    data = {
        "phone": "0987654321",
        "city_of_residence": "HCMC",
        "residential_address": "456 New Address"
    }

    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn("detail", response.data)
