from django.test import TestCase, RequestFactory
from rest_framework import status
from accounts.views import LoginView
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginViewTest(TestCase):
    def setUp(self):
        # Create a request factory to simulate HTTP requests
        self.factory = RequestFactory()

        # Initialize the LoginView as a view function
        self.view = LoginView.as_view()

        # Create a user for with a username and password
        self.user = User.objects.create_user(
            username='NhanTran',
            password='Abcd@1234'
        )

    def test_valid_login(self):
        data = {'username': 'NhanTran', 'password': 'Abcd@1234'}
        request = self.factory.post('/api/accounts/login/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_invalid_login(self):
        data = {'username': 'NhanTran', 'password': 'abcd@1234'}
        request = self.factory.post('/api/accounts/login/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_username(self):
        data = {'password': 'Abcd@1234'}
        request = self.factory.post('/api/accounts/login/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_missing_password(self):
        data = {'username': 'NhanTran'}
        request = self.factory.post('/api/accounts/login/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_invalid_request_data(self):
        data = {'username': 'nhantran', 'password': 'Abcd@1234'}
        request = self.factory.post('/api/accounts/login/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('username', response.data)

    def test_refresh_token_generation(self):
        data = {'username': 'NhanTran', 'password': 'Abcd@1234'}
        request = self.factory.post('/api/accounts/login/', data,
                                    format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
