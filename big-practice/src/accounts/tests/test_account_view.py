from django.test import TestCase, Client
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email/register.html')

    def test_register_view_post(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email/register.html')


class ActivateAccountTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
            is_active=False
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.activate_url = reverse('activate', kwargs={'uidb64': self.uid, 'token': self.token})

    def test_activate_account_valid(self):
        response = self.client.get(self.activate_url)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_account_invalid(self):
        invalid_token = 'invalid-token'
        activate_url = reverse('activate', kwargs={'uidb64': self.uid, 'token': invalid_token})
        response = self.client.get(activate_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email/activation_email.html')
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)


class LoginViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
            is_active=True
        )
        self.login_url = reverse('login')

    def test_login_view_post_invalid(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpass',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
