from django.urls import path

from apps.job.views import JobDetailView, JobListCreateView


urlpatterns = [
    path('list/', JobListCreateView.as_view(), name='job-list-create'),
    path('detail/<uuid:pk>/', JobDetailView.as_view(), name='job-detail'),
]
