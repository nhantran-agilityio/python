from django.urls import path

from apps.job.views import JobByUserView, JobListCreateView


urlpatterns = [
    path('', JobListCreateView.as_view(), name='job-list-create'),
    path('<uuid:user_id>/', JobByUserView.as_view(), name='job-by-user'),
]
