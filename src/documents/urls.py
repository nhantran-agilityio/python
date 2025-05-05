from django.urls import path

from documents.views import (
    DownloadAllDocumentsView,
    GetDocumentsAPIView,
    MultipleDocumentUploadView,
)

urlpatterns = [
    path('', GetDocumentsAPIView.as_view(),
         name='documents'),
    path('upload/', MultipleDocumentUploadView.as_view(),
         name='upload-documents'),

    path("download/", DownloadAllDocumentsView.as_view(),
         name="download-all"),
]
