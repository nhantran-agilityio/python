import os
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from apps.accounts.models import User, user_avatar_upload


class UserModelTest(TestCase):
    def setUp(self):
        self.url = reverse('register')
        self.user = User.objects.create(
            email='testuser@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            job_title='Developer',
            job_category='IT',
            department='Engineering',
            phone='1234567890',
            role='Admin',
            is_receive_newsletters=True,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.job_title, 'Developer')
        self.assertEqual(self.user.job_category, 'IT')
        self.assertEqual(self.user.department, 'Engineering')
        self.assertEqual(self.user.phone, '1234567890')
        self.assertEqual(self.user.role, 'Admin')
        self.assertTrue(self.user.is_receive_newsletters)
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser@example.com')

    def test_user_avatar_upload(self):
        filename = "avatar.jpg"
        expected_path = f'avatars/{self.user.id}.jpg'
        self.assertEqual(user_avatar_upload(self.user, filename), expected_path)

    def test_user_avatar_upload_with_different_extension(self):
        filename = 'avatar.jpg'
        expected_path = os.path.join('avatars/', f'{self.user.id}.jpg')
        self.assertEqual(user_avatar_upload(self.user, filename), expected_path)
