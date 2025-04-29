from django.test import TestCase
from job.models import Job
from job_responsibility.models import JobResponsibility
import uuid


class JobResponsibilityModelTest(TestCase):

    def setUp(self):
        # Create a test job
        self.job = Job.objects.create(
            name="Software Engineer",
            description="Develops and maintains software solutions.",
            department="Engineering",
            job_category="Full Time"
        )

        # Create a test job responsibility
        self.job_responsibility = JobResponsibility.objects.create(
            id=uuid.uuid4(),
            job=self.job,
            description="Responsible for code quality and development."
        )

    def test_job_responsibility_creation(self):
        """Test that a job responsibility is created successfully."""
        self.assertEqual(self.job_responsibility.job, self.job)
        self.assertEqual(self.job_responsibility.description, "Responsible for code quality and development.")
