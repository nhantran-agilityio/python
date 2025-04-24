import unittest
from unittest.mock import MagicMock
from constants.base import ROLE_ADMIN
from constants.enums import LeaveStatus
from utils.base import is_pending_recall, is_admin


class TestIsPendingRecall(unittest.TestCase):
    def test_is_pending_recall_true(self):
        instance = MagicMock(is_recalled=True, recall_status=LeaveStatus.PENDING)
        self.assertTrue(is_pending_recall(instance))

    def test_is_pending_recall_false_is_recalled_false(self):
        instance = MagicMock(is_recalled=False, recall_status=LeaveStatus.PENDING)
        self.assertFalse(is_pending_recall(instance))

    def test_is_pending_recall_false_recall_status_not_pending(self):
        instance = MagicMock(is_recalled=True, recall_status=LeaveStatus.APPROVED)
        self.assertFalse(is_pending_recall(instance))

    def test_is_pending_recall_false_both_false(self):
        instance = MagicMock(is_recalled=False, recall_status=LeaveStatus.APPROVED)
        self.assertFalse(is_pending_recall(instance))


class TestIsAdminFunction(unittest.TestCase):
    def test_admin_user(self):
        request = MagicMock()
        request.user = MagicMock()
        request.user.role = ROLE_ADMIN
        self.assertTrue(is_admin(request))

    def test_non_admin_user(self):
        request = MagicMock()
        request.user = MagicMock()
        request.user.role = 'non_admin'
        self.assertFalse(is_admin(request))

    def test_no_user_attribute(self):
        request = MagicMock()
        del request.user
        with self.assertRaises(AttributeError):
            is_admin(request)

    def test_no_role_attribute(self):
        request = MagicMock()
        request.user = MagicMock()
        del request.user.role
        with self.assertRaises(AttributeError):
            is_admin(request)
