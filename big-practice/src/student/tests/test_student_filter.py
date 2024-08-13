from django.test import TestCase
from datetime import date
from student.models import Student
from student.filters import StudentFilter


class TestStudentFilter(TestCase):
    def setUp(self):
        today = date.today()
        self.student1 = Student.objects.create(
            first_name='John',
            last_name='Doe',
            is_active=True,
            address="80 Le Cao Lang",
            email="test@gmail.com",
            gender="Male",
            birthday=date(today.year - 24, 1, 1),
        )
        self.student2 = Student.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            is_active=True,
            address="80 Le Cao Lang",
            gender="Male",
            birthday=date(today.year - 24, 1, 1),
        )

    def test_filter_by_first_name(self):
        filter = StudentFilter({'full_name': 'John'})
        queryset = filter.qs
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), self.student1)

    def test_filter_by_last_name(self):
        filter = StudentFilter({'full_name': 'Smith'})
        queryset = filter.qs
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), self.student2)

    def test_filter_by_no_match(self):
        filter = StudentFilter({'full_name': 'Fred'})
        queryset = filter.qs
        self.assertEqual(queryset.count(), 0)

    def test_filter_by_fullname(self):
        filter = StudentFilter({'full_name': 'John Doe'})
        queryset = filter.qs
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first(), self.student1)
