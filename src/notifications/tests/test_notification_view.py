from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from notification.models import Notification

User = get_user_model()


class NotificationViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="user@example.com", password="password123", username="user"
        )
        self.admin = User.objects.create_user(
            email="admin@example.com", password="password123", username="admin", role="admin"
        )

        self.notification_user = Notification.objects.create(
            user=self.user,
            message="Message for user"
        )
        self.notification_admin = Notification.objects.create(
            user=self.admin,
            message="Message for admin"
        )

    def test_list_user_notifications(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('notification-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], "Message for user")

    def test_list_admin_notifications(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('notification-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_notification(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "message": "New notification"
        }
        response = self.client.post(reverse('notification-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "New notification")

    def test_retrieve_own_notification(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse('notification-detail', kwargs={'pk': self.notification_user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Message for user")

    def test_retrieve_not_owned_notification(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse('notification-detail', kwargs={'pk': self.notification_admin.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})  # unauthorized → empty

    def test_patch_notification(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse('notification-detail', kwargs={'pk': self.notification_user.id}),
            {"is_read": True},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_read"])

    def test_delete_notification(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('notification-detail', kwargs={'pk': self.notification_user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Notification.objects.filter(pk=self.notification_user.id).exists())
