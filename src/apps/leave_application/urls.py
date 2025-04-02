from django.urls import path

from apps.leave_application.views import (
    LeaveApplicationByUserView,
    LeaveApplicationDetailView,
    LeaveApplicationListView,
    LeaveApplicationStatusUpdateView,
    LeaveApplicationDownloadView,
)

urlpatterns = [
    path(
        '',
        LeaveApplicationListView.as_view(),
        name='leave-application-list'
    ),
    path('<uuid:pk>/',
         LeaveApplicationDetailView.as_view(),
         name='leave-application-detail'),
    path(
        'users/<uuid:user_id>/',
        LeaveApplicationByUserView.as_view(),
        name='leave-application-by-user'
    ),
    path('<uuid:pk>/status/',
         LeaveApplicationStatusUpdateView.as_view(),
         name='leave-application-status-update'),
    path('download/<str:file_format>/',
         LeaveApplicationDownloadView.as_view(),
         name='leave-application-download'),

]
