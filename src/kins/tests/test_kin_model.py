
from django.test import TestCase
from kin.models import Kin
import uuid


class KinModelTest(TestCase):
    def setUp(self):
        # Create a test Kin instance
        self.kin = Kin.objects.create(
            id=uuid.uuid4(),
            name="John Doe",
            job="Software Engineer",
            phone="1234567890",
            relationship="Brother",
            residential_address="123 Main Street, New York"
        )

    def test_kin_creation(self):
        """Test that a Kin instance is created successfully."""
        self.assertEqual(self.kin.name, "John Doe")
        self.assertEqual(self.kin.job, "Software Engineer")
        self.assertEqual(self.kin.phone, "1234567890")
        self.assertEqual(self.kin.relationship, "Brother")
        self.assertEqual(self.kin.residential_address, "123 Main Street, New York")

    def test_kin_string_representation(self):
        """Test the string representation of the Kin instance."""
        self.assertEqual(str(self.kin), self.kin.name)
