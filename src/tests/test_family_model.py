from django.test import TestCase

from apps.accounts.models import Role, User
import uuid

from apps.family.models import Family


class FamilyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=uuid.uuid4(),
            email="testuser@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            phone="1234567890",
            role=Role.ADMIN,
            is_receive_newsletters=True,
        )

    def test_create_family_member(self):
        family_member = Family.objects.create(
            user=self.user,
            full_name="Test Family",
            relationship="Father",
            phone="1234567890",
            address="123 somewhere",
        )
        self.assertEqual(family_member.user, self.user)
