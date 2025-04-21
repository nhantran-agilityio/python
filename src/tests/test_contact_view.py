from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.contact.models import Contact
from apps.accounts.models import User


class ContactDetailAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            username="testuser"
        )

        self.client.login(username="testuser", password="testpass")
        self.contact = Contact.objects.create(
            phone_num_2="0123456789",
            city_of_residence="Test City",
            residential_address="Test Address"
        )
        self.user.contact = self.contact
        self.user.save()

        self.user_without_contact = User.objects.create_user(
            email='nocon@example.com',
            password='testpassword',
            first_name='No',
            username='no_contact',
            last_name='Contact'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_contact_detail_success(self):
        url = "/api/contacts/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_contact_detail_not_found(self):
        self.client.force_authenticate(user=self.user_without_contact)
        url = "/api/contacts/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_contact_success(self):
        url = "/api/contacts/"
        data = {
            "phone_num_2": "0987654321"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_num_2'], "0987654321")

    def test_patch_contact_not_found(self):
        self.client.force_authenticate(user=self.user_without_contact)
        url = "/api/contacts/"
        data = {
            "phone_num_2": "0123456789"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_contact_success(self):
        self.client.force_authenticate(user=self.user_without_contact)
        url = "/api/contacts/"
        data = {
            "phone_num_2": "0123456789",
            "city_of_residence": "Hanoi",
            "residential_address": "123 Street Name"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


def test_post_contact_invalid_data(self):
    self.client.force_authenticate(user=self.user_without_contact)
    url = "/api/contacts/"
    data = {
        "phone_num_2": "0123456789",
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('cityOfResidence', response.data)
    self.assertIn('residentialAddress', response.data)


def test_post_contact_when_already_exists(self):
    self.client.force_authenticate(user=self.user_with_contact)
    url = "/api/contacts/"

    data = {
        "phone_num_2": "0987654321",
        "city_of_residence": "HCMC",
        "residential_address": "456 New Address"
    }

    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn("detail", response.data)
