from django.test import TestCase
from contact.models import Contact


class ContactModelTest(TestCase):
    def setUp(self):
        # Create a test contact
        self.contact = Contact.objects.create(
            phone_num2="123456789",
            city_of_residence="New York",
            residential_address="123 Main Street"
        )

    def test_contact_creation(self):
        """Test that a contact is created successfully."""
        self.assertEqual(self.contact.phone_num2, "123456789")
        self.assertEqual(self.contact.city_of_residence, "New York")
        self.assertEqual(self.contact.residential_address, "123 Main Street")

    def test_contact_string_representation(self):
        """Test the string representation of the contact."""
        expected_representation = "123 Main Street"
        self.assertEqual(str(self.contact.residential_address), expected_representation)

    def test_contact_required_fields(self):
        with self.assertRaises(Exception):  # Test for missing residential_address
            Contact.objects.create(
                phone_num2="123456789",
                city_of_residence="New York",
                residential_address=None  # Missing required field
            )
