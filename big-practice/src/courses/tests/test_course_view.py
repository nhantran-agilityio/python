from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from datetime import timedelta

from courses.models import Course


class CourseViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()

        self.course = Course.objects.create(
            name='React',
            duration=timedelta(days=1, hours=5),
            description="This is react course")

    def test_get_course_list(self):
        response = self.client.get('/courses/?page=1')
        self.assertEqual(response.status_code, 200)

    def test_get_course_detail(self):
        response = self.client.get(f'/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'React')

    def test_create_course(self):
        data = {'name': 'React Native',
                'description': 'This is react native course',
                'duration': timedelta(days=1, hours=5)}
        response = self.client.post('/courses/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_course(self):
        data = {'name': 'Python',
                'description': 'This is Python course',
                'duration': timedelta(days=1, hours=5)}
        response = self.client.put(f'/courses/{self.course.pk}/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Course.objects.get(pk=self.course.pk).name, 'Python')

    def test_delete_course(self):
        response = self.client.delete(f'/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Course.objects.count(), 0)
