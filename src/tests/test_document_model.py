from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from apps.accounts.models import User
import uuid

from apps.document.models import Document


class DocumentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            username="testuser"
        )

        self.sample_file = SimpleUploadedFile(
            "test_doc.pdf", b"file_content_here", content_type="application/pdf"
        )

        self.document = Document.objects.create(
            user=self.user,
            document_type='offer_letter',
            document_file=self.sample_file
        )

    def test_document_creation(self):
        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(self.document.user, self.user)
        self.assertEqual(self.document.document_type, 'offer_letter')
        self.assertTrue(self.document.document_file.name.startswith('documents/test_doc'))

    def test_file_name_property(self):
        self.assertEqual(self.document.file_name, "test_doc.pdf")

    def test_file_path_property(self):
        # This will raise ValueError unless you use a real storage backend (e.g. S3 or MEDIA_URL config)
        self.assertIn('documents/test_doc.pdf', self.document.file_path)

    def test_str_representation(self):
        self.assertEqual(
            str(self.document),
            f"offer_letter - {self.document.document_file.name}"
        )
