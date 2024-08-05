from django.test import TestCase
from student.models import Student
from student.models import StudentManager

class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            first_name='Nhan',
            last_name='Tran',
            is_active=True,
            address="80 Le Cao Lang",
            email="test@gmail.com",
            gender="Male",
            birthday='1996-07-07',
        )
        self.student1 = Student.objects.create(
            first_name='John',
            last_name='Doe',
            is_active=True,
            address="123 Main St",
            email="john.doe@example.com",
            gender="Male",
            birthday='1990-01-01',
        )
        self.student2 = Student.objects.create(
            first_name='Jane',
            last_name='Smith',
            is_active=True,
            address="456 Elm St",
            email="jane.smith@example.com",
            gender="Female",
            birthday='1995-05-15',
        )

    def test_full_name(self):
        self.assertEqual(self.student.full_name, 'Nhan Tran')

    def test_student_creation(self):
        self.assertEqual(self.student.first_name, 'Nhan')
        self.assertEqual(self.student.last_name, 'Tran')
        self.assertEqual(self.student.email, 'test@gmail.com')
        self.assertEqual(self.student.address, '80 Le Cao Lang')
        self.assertEqual(self.student.gender, 'Male')
        self.assertEqual(self.student.birthday, '1996-07-07')
        self.assertTrue(self.student.is_active)

    def test_student_str_method(self):
        self.assertEqual(str(self.student), 'Nhan Tran')

    # def test_active_students(self):
    #     students = StudentManager.is_active()
    #     self.assertEqual(list(students), [self.student, self.student1, self.student2])

    # def test_student_avg_age(self):
    #     avg_age = StudentManager.student_avg_age()
    #     self.assertAlmostEqual(avg_age, 26.25, places=2)
