from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from apps.accounts.models import User
from django.test import RequestFactory
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from apps.accounts.views import activate_account


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = "/api/accounts/register/"
        self.user_data = {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User',
            'phone': '1234567890',
            'is_receive_newsletters': True
        }

    def test_register_user_success(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_register_user_password_mismatch(self):
        self.user_data['confirm_password'] = 'differentpassword'
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Passwords do not match.')


class ActivateAccountViewTest(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email='test@example.com', username='testuser')
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_activate_account_success(self):
        request = self.factory.get(reverse('activate', kwargs={'uidb64': self.uidb64, 'token': self.token}))
        response = activate_account(request, self.uidb64, self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Account activated successfully.'})
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_account_invalid_token(self):
        invalid_token = 'invalid-token'
        request = self.factory.get(reverse('activate', kwargs={'uidb64': self.uidb64, 'token': invalid_token}))
        response = activate_account(request, self.uidb64, invalid_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid or expired token.'})

    def test_activate_account_non_existent_user(self):
        non_existent_uidb64 = "397d17e4-dea0-4b54-b35a-87d72b17e95a"
        request = self.factory.get(reverse('activate', kwargs={'uidb64': non_existent_uidb64, 'token': self.token}))
        response = activate_account(request, non_existent_uidb64, self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid or expired token.'})

    def test_activate_account_invalid_uidb64(self):
        invalid_uidb64 = 'invalid-uidb64'
        request = self.factory.get(reverse('activate', kwargs={'uidb64': invalid_uidb64, 'token': self.token}))
        response = activate_account(request, invalid_uidb64, self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid or expired token.'})


class LoginViewTest(APITestCase):
    def test_login_success(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="password",
            username="testuser",
        )

        response = self.client.post(
            reverse("login"),
            data={
                "email": user.email,
                "password": "password"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            data={
                "email": "testexample.com",
                "password": "wrongpassword"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
