from django.test import TestCase
from leave_applications.models import LeaveApplication
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()


class TestSendLeaveRecallNotification(TestCase):
    def setUp(self):
        self.employee = User.objects.create_user('employee', 'employee@example.com', 'password')
        self.relief_officer = User.objects.create_user('relief_officer', 'relief_officer@example.com', 'password')

    def test_notification_sent_when_leave_is_recalled(self):
        leave = LeaveApplication.objects.create(
            employee=self.employee,
            relief_officer=self.relief_officer,
            type="Annual",
            reason="Sick leave",
            start_date="2022-01-01",
            end_date="2022-01-05",
            durations=5,
            recall_status="Pending",
            resumption_date="2022-01-05",
            is_recalled=True,
        )
        self.assertTrue(leave.is_pending_recall)
        self.assertEqual(Notification.objects.count(), 1)

    def test_notification_not_sent_when_leave_is_not_recalled(self):
        leave = LeaveApplication.objects.create(
            employee=self.employee,
            relief_officer=self.relief_officer,
            type="Annual",
            reason="Sick leave",
            start_date="2022-01-01",
            end_date="2022-01-05",
            durations=5,
            recall_status="Approved",
            resumption_date="2022-01-05",
            is_recalled=False,
        )
        self.assertFalse(leave.is_pending_recall)
        self.assertEqual(Notification.objects.count(), 0)

    def test_notification_sent_with_correct_message_when_relief_officer_is_present(self):
        leave = LeaveApplication.objects.create(
            employee=self.employee,
            relief_officer=self.relief_officer,
            type="Annual",
            reason="Sick leave",
            start_date="2022-01-01",
            end_date="2022-01-05",
            durations=5,
            recall_status="Pending",
            resumption_date="2022-01-05",
            is_recalled=True,
        )
        notification = Notification.objects.first()
        self.assertEqual(notification.message, f"Your {leave.type} leave has been recalled by {self.relief_officer.first_name} {self.relief_officer.last_name}. Please return before {leave.end_date}.")

    def test_notification_sent_with_correct_message_when_relief_officer_is_not_present(self):
        leave = LeaveApplication.objects.create(
            employee=self.employee,
            relief_officer=None,
            type="Annual",
            reason="Sick leave",
            start_date="2022-01-01",
            end_date="2022-01-05",
            durations=5,
            recall_status="Pending",
            resumption_date="2022-01-05",
            is_recalled=True,
        )
        notification = Notification.objects.first()
        self.assertEqual(notification.message, f"Your {leave.type} leave has been recalled by an unknown officer. Please return before {leave.end_date}.")

    def test_notification_sent_to_correct_user(self):
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.employee)
