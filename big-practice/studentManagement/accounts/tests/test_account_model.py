from django.test import TestCase
from accounts.models import User

class UserModelTest(TestCase):
    # def setUp(self):

        # self.user = User.objects.create(
        #     first_name='Nhan',
        #     last_name='Tran',
        #     is_active=True,
        #     address="80 Le Cao Lang",
        #     email="test@gmail.com",
        #     gender="Male",
        #     birthday="2000-0101"
        # )

    def test_valid_email(self):
        user = User(email="test@example.com")
        self.assertEqual(str(user), "test@example.com")

    def test_empty_email(self):
        user = User(email="")
        self.assertEqual(str(user), "")

    # def test_none_email(self):
    #     user = User(email=None)
    #     self.assertEqual(str(user), "None")
