from django.urls import path
from .views import JobResponsibilityListCreateView, JobResponsibilityDetailView

urlpatterns = [
    path('job-responsibilities/',
         JobResponsibilityListCreateView.as_view(),
         name='job-responsibility-list-create'),
    path('job-responsibilities/<int:pk>/',
         JobResponsibilityDetailView.as_view(),
         name='job-responsibility-detail'),
]
