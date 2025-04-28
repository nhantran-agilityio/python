
from django.test import TestCase
from education.models import Education, EducationType
from accounts.models import User
from django.utils import timezone


class EducationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="testuser@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            phone="1234567890"
        )

    def test_education_creation(self):
        education = Education.objects.create(
            user=self.user,
            name="BSc Computer Science",
            department="Computer Science",
            course="Algorithms",
            location="University of Test",
            start_date=timezone.now().date(),
            description="A course on algorithms.",
            type=EducationType.ACADEMIC
        )
        self.assertEqual(education.name, "BSc Computer Science")
        self.assertEqual(education.user, self.user)
        self.assertEqual(education.type, EducationType.ACADEMIC)

    def test_end_date_can_be_null(self):
        education = Education.objects.create(
            user=self.user,
            name="BSc Computer Science",
            department="Computer Science",
            course="Algorithms",
            location="University of Test",
            start_date=timezone.now().date(),
            end_date=None,
            description="A course on algorithms.",
            type=EducationType.ACADEMIC
        )
        self.assertIsNone(education.end_date)
