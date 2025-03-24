from django.urls import path
from .views import MultipleDocumentUploadView

urlpatterns = [
    path('upload/', MultipleDocumentUploadView.as_view(),
         name='upload-documents'),
]
