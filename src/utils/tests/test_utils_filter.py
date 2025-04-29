from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from leave_application.models import LeaveApplication
from utils.filter import filter_leave_applications

User = get_user_model()


class FilterLeaveApplicationsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            first_name='John',
            last_name='Doe',
            email='U4f7u@example.com',
            role='employee',
            password='pass'
        )
        self.other_user = User.objects.create_user(
            username='seconduser',
            first_name='Alice',
            last_name='Smith',
            role='employee',
            password='pass'
        )

        today = timezone.now().date()

        self.leave1 = LeaveApplication.objects.create(
            employee=self.user,
            type='Annual',
            start_date=today,
            end_date=today,
            durations=1,
            resumption_date=today,
            reason='Vacation',
            status='Approved'
        )

        self.leave2 = LeaveApplication.objects.create(
            employee=self.user,
            type='Sick',
            start_date=today,
            end_date=today,
            durations=1,
            resumption_date=today,
            reason='Sick leave',
            status='Pending'
        )

        self.recall_leave = LeaveApplication.objects.create(
            employee=self.other_user,
            type='Annual',
            start_date=today,
            end_date=today,
            durations=1,
            resumption_date=today,
            reason='Emergency',
            status='Approved'
        )

    def test_filter_by_employee_name(self):
        queryset = LeaveApplication.objects.select_related('employee').all()
        filtered = filter_leave_applications(queryset, employee_name='john')
        self.assertIn(self.leave1, filtered)
        self.assertIn(self.leave2, filtered)
        self.assertNotIn(self.recall_leave, filtered)

    def test_filter_by_type(self):
        queryset = LeaveApplication.objects.select_related('employee').all()
        filtered = filter_leave_applications(queryset, leave_types='Annual')
        self.assertIn(self.leave1, filtered)
        self.assertIn(self.recall_leave, filtered)
        self.assertNotIn(self.leave2, filtered)

    def test_filter_by_is_recall(self):
        queryset = LeaveApplication.objects.select_related('employee').all()
        filtered = filter_leave_applications(queryset, is_recall=True)
        self.assertIn(self.leave1, filtered)
        self.assertIn(self.recall_leave, filtered)
        self.assertNotIn(self.leave2, filtered)

    def test_combined_filters(self):
        queryset = LeaveApplication.objects.select_related('employee').all()
        filtered = filter_leave_applications(queryset, employee_name='john', leave_types='Annual', is_recall=True)
        self.assertEqual(len(filtered), 1)
        self.assertIn(self.leave1, filtered)
        self.assertNotIn(self.leave2, filtered)
        self.assertNotIn(self.recall_leave, filtered)
