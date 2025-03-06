# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth.models import User
# from instructors.models import Instructor

# class InstructorViewTests(APITestCase):

#     def setUp(self):
#         self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
#         self.client.login(username='admin', password='adminpass')
#         self.instructor = Instructor.objects.create(user=self.admin_user, name='Test Instructor')

#     def test_create_instructor(self):
#         url = reverse('instructor-create')
#         data = {'user': self.admin_user.id, 'name': 'New Instructor'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Instructor.objects.count(), 2)
#         self.assertEqual(Instructor.objects.get(id=response.data['id']).name, 'New Instructor')

#     def test_update_instructor(self):
#         url = reverse('instructor-update', args=[self.instructor.id])
#         data = {'name': 'Updated Instructor'}
#         response = self.client.put(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.instructor.refresh_from_db()
#         self.assertEqual(self.instructor.name, 'Updated Instructor')

#     def test_delete_instructor(self):
#         url = reverse('instructor-delete', args=[self.instructor.id])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Instructor.objects.count(), 0)
