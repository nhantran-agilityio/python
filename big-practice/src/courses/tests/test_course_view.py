from django.test import TestCase
from datetime import date
from rest_framework import status
from courses.models import Course
from student.models import Student
from instructors.models import Instructor
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()


class CourseViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', password='adminpass'
        )
        self.client.login(username='admin', password='adminpass')
        self.instructor = Instructor.objects.create(
            user=self.admin_user, name='Test Instructor'
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description'
        )
        self.course.instructors.add(self.instructor)
        self.student = Student.objects.create(
            user=self.admin_user,
            first_name='Test',
            last_name='Student',
            email='test@student.com',
            birthday=date(2000, 1, 1)
        )

    def test_create_course(self):
        url = reverse('course-list')
        data = {
            'name': 'New Course',
            'description': 'New Description',
            'instructors': [self.instructor.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        course_name = Course.objects.get(id=response.data['id']).name
        self.assertEqual(course_name, 'New Course')

    def test_delete_course(self):
        response = self.client.delete(f'/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Course.objects.count(), 0)
