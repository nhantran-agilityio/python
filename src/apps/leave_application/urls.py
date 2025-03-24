from django.urls import path

from apps.leave_application.views import (
    LeaveApplicationByUserView,
    LeaveApplicationListView,
)

urlpatterns = [
    path(
        '',
        LeaveApplicationListView.as_view(),
        name='leave-application-list'
    ),
    path(
        'users/<uuid:user_id>/',
        LeaveApplicationByUserView.as_view(),
        name='leave-application-by-user'
    ),
]
