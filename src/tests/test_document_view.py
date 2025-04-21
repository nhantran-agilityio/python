from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch
from apps.accounts.models import User
from apps.document.models import Document
from django.core.files.uploadedfile import SimpleUploadedFile


class TestDocumentBaseView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            username="testuser"
        )

        self.client.login(username="testuser", password="testpass")
        self.url = '/api/documents/'

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_validate_document_type_success(self):
        doc_type = 'OfferLetter'
        response = self.client.get(f"{self.url}?doc_type={doc_type}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MultipleDocumentUploadViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            username="testuser"
        )

        self.client.login(username="testuser", password="testpass")
        self.url = '/api/documents/'

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_upload_multiple_documents(self):
        url = '/api/documents/upload/'
        files = {
            f"documents[offerLetter]": SimpleUploadedFile("offer_letter.pdf", b"file_content", content_type="application/pdf"),
            f"documents[birthCertificate]": SimpleUploadedFile("birth_certificate.pdf", b"file_content", content_type="application/pdf"),
        }

        response = self.client.post(url, files)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 2)
        self.assertIn("Files uploaded successfully!", response.data["message"])

    def test_patch_update_documents(self):
        Document.objects.create(user=self.user, document_type='offer_letter', document_file=SimpleUploadedFile("old_offer_letter.pdf", b"old_file_content", content_type="application/pdf"))

        url = '/api/documents/upload/'
        files = {
            f"documents[offerLetter]": SimpleUploadedFile("new_offer_letter.pdf", b"new_file_content", content_type="application/pdf"),
        }

        response = self.client.patch(url, files)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Document.objects.count(), 1)
        self.assertIn("Documents updated successfully!", response.data["message"])
        self.assertTrue(Document.objects.filter(document_file__icontains="new_offer_letter.pdf").exists())

    def test_no_documents_provided(self):
        url = '/api/documents/upload/'
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No documents provided.", response.data["error"])


class DownloadAllDocumentsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            username="testuser"
        )

        self.client.login(username="testuser", password="testpass")
        self.url = '/api/documents/download-all/'

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_download_no_documents(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("No documents found to download.", response.data["message"])

    def test_download_with_documents(self):
        dummy_pdf = SimpleUploadedFile("dummy.pdf", b"Fake PDF content", content_type="application/pdf")
        Document.objects.create(user=self.user, document_type="offer_letter", document_file=dummy_pdf)
        Document.objects.create(user=self.user, document_type="birth_certificate", document_file=dummy_pdf)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/zip")
        self.assertIn("Content-Disposition", response)
        self.assertIn(f'{self.user.username}_documents.zip', response["Content-Disposition"])

    @patch("apps.document.views.DocumentBaseView.validate_document_type")
    def test_valid_upload(self, mock_validate):
        mock_validate.return_value = ("birth_certificate", None)
        file = SimpleUploadedFile("file.pdf", b"dummy content", content_type="application/pdf")
        response = self.client.patch(self.url, {"documents[birth_certificate]": file}, format="multipart")
        # Add assertions based on your actual success behavior
        self.assertNotEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
