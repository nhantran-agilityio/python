from django.test import TestCase
from instructors.models import Instructor


class InstructorModelTest(TestCase):

    def setUp(self):
        self.instructor = Instructor.objects.create(
            name='John Doe',
            email='john.doe@example.com',
            is_active=True
        )

    def test_instructor_creation(self):
        self.assertEqual(self.instructor.name, 'John Doe')
        self.assertEqual(self.instructor.email, 'john.doe@example.com')
        self.assertTrue(self.instructor.is_active)

    def test_instructor_str(self):
        self.assertEqual(str(self.instructor), 'John Doe')

    def test_instructor_is_active_default(self):
        instructor = Instructor.objects.create(
            name='Jane Doe',
            email='jane.doe@example.com'
        )
        self.assertTrue(instructor.is_active)
