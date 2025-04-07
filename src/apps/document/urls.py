from django.urls import path
from .views import DownloadAllDocumentsView, MultipleDocumentUploadView

urlpatterns = [
    path('upload/', MultipleDocumentUploadView.as_view(),
         name='upload-documents'),

    path("download-all/", DownloadAllDocumentsView.as_view(),
         name="download-all"),
]
