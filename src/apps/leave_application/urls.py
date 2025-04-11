from django.urls import path
from apps.leave_application.views import (
    LeaveApplicationByUserView,
    LeaveApplicationDetailAPIView,
    LeaveApplicationListAPIView,
    LeaveApplicationStatusUpdateView,
    RecallApplicationStatusUpdateView,
    LeaveApplicationDownloadView,
)

urlpatterns = [
    path(
        '',
        LeaveApplicationListAPIView.as_view(),
        name='leave-application'
    ),
    path(
        '<uuid:pk>/',
        LeaveApplicationDetailAPIView.as_view(),
        name='leave-application-detail'
    ),
    path(
        '<uuid:pk>/status/',
        LeaveApplicationStatusUpdateView.as_view(),
        name='leave-application-status-update'
    ),
    path(
        '<uuid:pk>/recall-status/',
        RecallApplicationStatusUpdateView.as_view(),
        name='recall-application-status-update'
    ),

    path(
        'users/<uuid:user_id>/',
        LeaveApplicationByUserView.as_view(),
        name='leave-application-by-user'
    ),
    path(
        'download/<str:file_format>/',
        LeaveApplicationDownloadView.as_view(),
        name='leave-application-download'
    ),
    path(
        'history/download/<uuid:user_id>/<str:file_format>/',
        LeaveApplicationDownloadView.as_view(),
        name='leave-history-download'
    ),
]
