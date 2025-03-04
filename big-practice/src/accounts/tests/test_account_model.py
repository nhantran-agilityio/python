from django.test import TestCase
from django.utils import timezone
from accounts.models import User


class UserModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            is_active=True,
            is_Admin=True,
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.is_Admin)
        self.assertIsInstance(self.user.created_at, timezone.datetime)
        self.assertIsInstance(self.user.updated_at, timezone.datetime)

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser@example.com')
