from django.test import TestCase
from accounts.models import User


class UserModelTest(TestCase):
    fixtures = ['accounts.json']

    def test_valid_email(self):
        user = User(email="test@example.com")
        self.assertEqual(str(user), "test@example.com")

    def test_empty_email(self):
        user = User(email="")
        self.assertEqual(str(user), "")
