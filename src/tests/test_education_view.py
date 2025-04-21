from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.education.models import Education


class EducationViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            username="testuser"
        )


        self.other_user = User.objects.create_user(email="testuser+01@example.com", username='otheruser', password='password')
        self.education = Education.objects.create(
            user=self.user,
            name='Test Education',
            department='Test Department',
            course='Test Course',
            location='Test Location',
            start_date='2023-01-01',
            end_date='2023-12-31',
            description='Test Description',
            type='Academic'
        )
        self.client.login(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_queryset(self):
        url='/api/educations/'
        response = self.client.get((url), {'user_id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(url, {'type': 'Academic'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(url, {'type': 'Professional'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_perform_create(self):
        url='/api/educations/'
        self.client.login(username='staffuser', password='password')
        response = self.client.post(url, {
            'name': 'New Education',
            'department': 'New Department',
            'course': 'New Course',
            'location': 'New Location',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'description': 'New Description',
            'type': 'Academic',
            'user_id': self.other_user.id
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.login(username='testuser', password='password')
        response = self.client.post(url, {
            'name': 'New Education',
            'department': 'New Department',
            'course': 'New Course',
            'location': 'New Location',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'description': 'New Description',
            'type': 'Academic'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
