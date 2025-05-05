# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from leave_application.views import (
    LeaveApplicationDownloadView,
    LeaveApplicationViewSet,
    RecallLeaveApplicationView,
)

router = DefaultRouter()
router.register('', LeaveApplicationViewSet, basename='leave_application')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'download/<str:file_format>/',
        LeaveApplicationDownloadView.as_view(),
        name='leave-application-download',
    ),
    path(
        '<uuid:pk>/recall/',
        RecallLeaveApplicationView.as_view(),
        name='recall-leave-application',
    ),
]
