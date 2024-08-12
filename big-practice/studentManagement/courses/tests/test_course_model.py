import unittest
from courses.models import Course


class CourseModelTest(unittest.TestCase):

    def test_not_empty_course_name(self):
        course = Course(name='Test Course')
        self.assertEqual(str(course), 'Test Course')

    def test_empty_course_name(self):
        course = Course(name='')
        self.assertEqual(str(course), '')
