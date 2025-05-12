from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

from family.models import Family

User = get_user_model()


class FamilyViewSetTest(APITestCase):

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

        self.family = Family.objects.create(
            user=self.user,
            full_name="Nguyen Van A",
            relationship="Father",
            phone="0901234567",
            address="123 Le Loi"
        )

    def test_retrieve_family_not_found(self):
        url = '/api/family/999/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_create_family(self):
        url = reverse('family-list')
        payload = {
            "full_name": "Nguyen Van B",
            "relationship": "Mother",
            "phone": "0987654321",
            "address": "456 Tran Hung Dao"
        }
        response = self.client.post(url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["full_name"], payload["full_name"])
        self.assertEqual(Family.objects.count(), 2)
        self.assertEqual(Family.objects.last().user, self.user)

    def test_get_queryset_only_returns_user_families(self):
        Family.objects.create(
            user=self.other_user,
            full_name="Not Yours",
            relationship="Stranger",
            phone="000000000",
            address="Unknown"
        )

        url = reverse('family-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Only 1 record should belong to self.user
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["full_name"], self.family.full_name)
