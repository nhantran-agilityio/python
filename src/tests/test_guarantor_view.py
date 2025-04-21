from rest_framework.test import APITestCase
from rest_framework import status
from apps.guarantor.models import Guarantor
from apps.accounts.models import User
from rest_framework.test import APIClient
import uuid


class GuarantorViewSetTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            id=uuid.uuid4(),
            email="testuser@example.com",
            username="testuser",
            password="password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a test Guarantor instance
        self.guarantor = Guarantor.objects.create(
            user=self.user,
            name="John Doe",
            job="Software Engineer",
            phone="1234567890"
        )

        # Define URLs
        self.list_url = "/api/guarantors/"
        self.detail_url = f"/api/guarantors/{self.guarantor.id}/"

    def test_list_guarantors(self):
        """Test listing all Guarantor instances for the authenticated user."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "John Doe")

    def test_create_guarantor(self):
        """Test creating a new Guarantor instance."""
        data = {
            "name": "Jane Doe",
            "job": "Doctor",
            "phone": "9876543210"
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Jane Doe")
        self.assertEqual(response.data["job"], "Doctor")
        self.assertEqual(Guarantor.objects.filter(name="Jane Doe").count(), 1)

    def test_update_guarantor(self):
        """Test updating an existing Guarantor instance."""
        data = {
            "name": "John Smith",
            "job": "Manager",
            "phone": "1234567890"
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "John Smith")
        self.assertEqual(response.data["job"], "Manager")
        self.guarantor.refresh_from_db()
        self.assertEqual(self.guarantor.name, "John Smith")
        self.assertEqual(self.guarantor.job, "Manager")

    def test_delete_guarantor(self):
        """Test deleting a Guarantor instance."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Guarantor.objects.filter(id=self.guarantor.id).count(), 0)
