from django.urls import path
from .views import DownloadAllDocumentsView, MultipleDocumentUploadView, GetDocumentsAPIView

urlpatterns = [
    path('', GetDocumentsAPIView.as_view(),
         name='documents'),
    path('upload/', MultipleDocumentUploadView.as_view(),
         name='upload-documents'),

    path("download-all/", DownloadAllDocumentsView.as_view(),
         name="download-all"),
]
