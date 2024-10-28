from django.test import TestCase
from datetime import date
from student.models import Student


class StudentModelTest(TestCase):
    def setUp(self):
        today = date.today()
        fixtures = ['student.json']
        print("studentMock", fixtures)
        self.student = Student.objects.create(
            first_name='Nhan',
            last_name='Tran',
            is_active=True,
            address="80 Le Cao Lang",
            email="test@gmail.com",
            gender="Male",
            birthday=date(today.year - 24, 1, 1),
        )
        self.student1 = Student.objects.create(
            first_name='John',
            last_name='Doe',
            is_active=True,
            address="123 Main St",
            email="john.doe@example.com",
            gender="Male",
            # birthday='1990-01-01',
            birthday=date(today.year - 18, 1, 1),
        )
        self.student2 = Student.objects.create(
            first_name='Jane',
            last_name='Smith',
            is_active=True,
            address="456 Elm St",
            email="jane.smith@example.com",
            gender="Female",
            # birthday='1995-05-15',
            birthday=date(today.year - 24, 1, 1),
        )

    def test_full_name(self):
        self.assertEqual(self.student.full_name, 'Nhan Tran')

    def test_student_creation(self):
        self.assertEqual(self.student.first_name, 'Nhan')
        self.assertEqual(self.student.last_name, 'Tran')
        self.assertEqual(self.student.email, 'test@gmail.com')
        self.assertEqual(self.student.address, '80 Le Cao Lang')
        self.assertEqual(self.student.gender, 'Male')
        self.assertEqual(self.student.birthday, date(2000, 1, 1))
        self.assertTrue(self.student.is_active)

    def test_student_str_method(self):
        self.assertEqual(str(self.student), 'Nhan Tran')

    def test_active_students(self):
        # Fetch active students
        active_students = Student.objects.active_Students()

        # Check that the correct students are returned
        self.assertEqual(active_students.count(), 3)
        self.assertTrue(active_students.filter(first_name="Nhan").exists())

    def test_get_age(self):
        # Calculate expected age
        today = date.today()
        expected_age = today.year - self.student.birthday.year - (
            (today.month, today.day) < (self.student.birthday.month,
                                        self.student.birthday.day))

        # Test if the calculated age matches
        self.assertEqual(self.student.get_age(), expected_age)

    def test_student_older_than_20(self):
        students_older_than_20 = Student.objects.student_over_20()

        self.assertIn(self.student, students_older_than_20)
        self.assertNotIn(self.student1, students_older_than_20)

    def test_student_avg_age(self):
        """Test the student_avg_age manager method."""
        # Ensure that the average age is calculated correctly
        self.assertEqual(
            Student.objects.student_avg_age(), 22
        )  # Assuming the current year is 2021
