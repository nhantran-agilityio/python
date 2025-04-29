from django.test import TestCase
from accounts.models import User
import uuid

from guarantor.models import Guarantor


class GuarantorModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            id=uuid.uuid4(),
            email="testuser@example.com",
            username="testuser",
            password="password123"
        )

        # Create a test Guarantor instance
        self.guarantor = Guarantor.objects.create(
            user=self.user,
            name="John Doe",
            job="Software Engineer",
            phone="1234567890"
        )

    def test_guarantor_creation(self):
        """Test that a Guarantor instance is created successfully."""
        self.assertEqual(self.guarantor.name, "John Doe")
        self.assertEqual(self.guarantor.job, "Software Engineer")
        self.assertEqual(self.guarantor.phone, "1234567890")
        self.assertEqual(self.guarantor.user, self.user)

    def test_guarantor_string_representation(self):
        """Test the string representation of the Guarantor instance."""
        self.assertEqual(str(self.guarantor), "John Doe")
