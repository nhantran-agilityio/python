from django.test import TestCase
from accounts.models import User
from jobs.models import Job


class JobModelTest(TestCase):
    def setUp(self):
        # Create a test user for line management
        self.user = User.objects.create(
            email="manager@example.com",
            username="manager",
            first_name="Manager",
            last_name="User",
            phone="1234567890",
            role="Admin",
        )

        # Create a test job
        self.job = Job.objects.create(
            name="Software Engineer",
            description="Responsible for developing software solutions.",
            department="Engineering",
            line_management=self.user,  # Assign the User instance
            job_category="Full Time",
        )

    def test_job_creation(self):
        """Test that a job is created successfully."""
        self.assertEqual(self.job.name, "Software Engineer")
        self.assertEqual(self.job.description, "Responsible for developing software solutions.")
        self.assertEqual(self.job.department, "Engineering")
        self.assertEqual(self.job.line_management, self.user)  # Check the User instance
        self.assertEqual(self.job.job_category, "Full Time")

    def test_job_string_representation(self):
        """Test the string representation of the job."""
        self.assertEqual(str(self.job), "Software Engineer")
