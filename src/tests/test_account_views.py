from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = "/api/accounts/register/"
        self.user_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpassword',
            'confirm_password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User',
            'job_title': 'Developer',
            'job_category': 'IT',
            'department': 'Engineering',
            'phone': '1234567890',
            'role': 'Admin',
            'is_receive_newsletters': True
        }

    def test_register_user_success(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully')
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_register_user_password_mismatch(self):
        self.user_data['confirm_password'] = 'differentpassword'
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Passwords do not match.')
