from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification
import uuid

User = get_user_model()


class NotificationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="testpass123"
        )

    def test_create_notification_basic(self):
        notification = Notification.objects.create(
            user=self.user,
            message="You have a new notification!"
        )

        self.assertIsNotNone(notification.id)
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, "You have a new notification!")
        self.assertFalse(notification.is_read)
        self.assertIsNotNone(notification.created_at)
        self.assertIsNone(notification.recall_id)

    def test_create_notification_with_recall_id(self):
        recall_uuid = uuid.uuid4()

        notification = Notification.objects.create(
            user=self.user,
            message="Test with recall_id",
            recall_id=recall_uuid
        )

        self.assertEqual(notification.recall_id, recall_uuid)

    def test_str_representation(self):
        notification = Notification.objects.create(
            user=self.user,
            message="Test __str__"
        )

        self.assertEqual(str(notification), "Notification for testuser")
