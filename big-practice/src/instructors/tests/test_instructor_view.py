from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from instructors.models import Instructor


class InstructorViewTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password'
        )
        self.client = APIClient()
        self.client.login(username='admin', password='password')

    def test_create_instructor(self):
        url = reverse('instructor-create')
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Instructor.objects.count(), 1)
        self.assertEqual(Instructor.objects.get().name, 'John Doe')

    def test_update_instructor(self):
        instructor = Instructor.objects.create(
            name='John Doe', email='john.doe@example.com'
        )
        url = reverse('instructor-update', args=[instructor.id])
        data = {'name': 'Jane Doe', 'email': 'jane.doe@example.com'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        instructor.refresh_from_db()
        self.assertEqual(instructor.name, 'Jane Doe')
        self.assertEqual(instructor.email, 'jane.doe@example.com')

    def test_delete_instructor(self):
        instructor = Instructor.objects.create(
            name='John Doe', email='john.doe@example.com'
        )
        url = reverse('instructor-delete', args=[instructor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Instructor.objects.count(), 0)
