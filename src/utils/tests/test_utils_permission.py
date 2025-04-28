from django.test import TestCase
from accounts.models import User
from utils.custom_permissions import IsAdmin, IsEmployee


class TestIsEmployeePermission(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser1@example.com',
            password='secret',
            role='employee'
        )

    def test_permission_allowed(self):
        request = self.client.request()
        request.user = self.user

        permission = IsEmployee()
        self.assertTrue(permission.has_permission(request, None))

    def test_permission_denied(self):
        request = self.client.request()
        request.user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='secret',
            role='admin'
        )

        permission = IsEmployee()
        self.assertFalse(permission.has_permission(request, None))


class TestIsAdminPermission(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser3',
            email='testuser3@example.com',
            password='secret',
            role='admin'
        )

    def test_permission_allowed(self):
        request = self.client.request()
        request.user = self.user

        permission = IsAdmin()
        self.assertTrue(permission.has_permission(request, None))

    def test_permission_denied(self):
        request = self.client.request()
        request.user = User.objects.create_user(
            username='testuser4',
            email='testuser4@example.com',
            password='secret',
            role='employee'
        )

        permission = IsAdmin()
        self.assertFalse(permission.has_permission(request, None))
