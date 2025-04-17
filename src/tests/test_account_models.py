from django.test import TestCase
from apps.accounts.models import User, Role
import uuid


class UserModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(
            id=uuid.uuid4(),
            email="testuser@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            phone="1234567890",
            role=Role.ADMIN,
            is_receive_newsletters=True,
        )

    def test_user_creation(self):
        """Test that a user is created successfully."""
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.phone, "1234567890")
        self.assertEqual(self.user.role, Role.ADMIN)
        self.assertTrue(self.user.is_receive_newsletters)

    def test_user_string_representation(self):
        """Test the string representation of the user."""
        self.assertEqual(str(self.user), "testuser@example.com")

    def test_user_default_role(self):
        """Test that the default role is None if not provided."""
        user_without_role = User.objects.create(
            id=uuid.uuid4(),
            email="noroleuser@example.com",
            username="noroleuser",
            first_name="No",
            last_name="Role",
            phone="0987654321",
        )
        self.assertIsNone(user_without_role.role)

    def test_user_required_fields(self):
        """Test that required fields are validated."""
        with self.assertRaises(Exception):
            User.objects.create(
                email=None,  # Email is required
                username="invaliduser",
                first_name="Invalid",
                last_name="User",
            )
