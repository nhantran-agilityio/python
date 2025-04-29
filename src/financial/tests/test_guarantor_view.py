from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

from guarantor.models import Guarantor

User = get_user_model()


class GuarantorViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            username="testuser",
            first_name="Test",
            last_name="User"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass456",
            username="testuser",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.guarantor = Guarantor.objects.create(
            user=self.user,
            name="John Doe",
            job="Software Engineer",
            phone="1234567890"
        )

    def test_retrieve_guarantor_not_found(self):

        url = '/api/guarantors/999/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_create_guarantor(self):
        url = '/api/guarantors/'
        payload = {
            "name": "John Doe",
            "job": "Software Engineer",
            "phone": "1234567890"
        }
        response = self.client.post(url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Guarantor.objects.count(), 2)
        self.assertEqual(Guarantor.objects.last().user, self.user)

    def test_get_queryset_only_returns_user_guarantors(self):
        Guarantor.objects.create(
            user=self.other_user,
            name="Doe",
            job="Software Engineer",
            phone="1234567690"
        )

        url = '/api/guarantors/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
