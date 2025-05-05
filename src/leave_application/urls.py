from django.urls import path
from leave_application.views import (
    LeaveApplicationDetailAPIView,
    LeaveApplicationListAPIView,
    LeaveApplicationStatusUpdateView,
    LeaveApplicationDownloadView,
    RecallLeaveApplicationView,
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
        'download/<str:file_format>/',
        LeaveApplicationDownloadView.as_view(),
        name='leave-application-download'
    ),
    path('<uuid:pk>/recall/', RecallLeaveApplicationView.as_view(), name='recall-leave-application'),
]
