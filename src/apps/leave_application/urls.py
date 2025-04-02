from django.urls import path

from apps.leave_application.views import (
    LeaveApplicationByUserView,
    LeaveApplicationDeleteView,
    LeaveApplicationDetailView,
    LeaveApplicationEditView,
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
    path('<uuid:pk>/update', LeaveApplicationEditView.as_view(),
         name='leave-application-edit'),  # Edit endpoint
    path('<uuid:pk>/delete', LeaveApplicationDeleteView.as_view(),
         name='leave-application-delete'),  # Delete endpoint
    path('history/download/<uuid:user_id>/<str:file_format>/',
         LeaveApplicationDownloadView.as_view(), name='leave-history-download')

]
