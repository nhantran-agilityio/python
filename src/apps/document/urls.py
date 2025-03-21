from django.urls import path
from apps.document.views import DocumentUploadView

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
]
