from django.urls import path
from .views import NotificationDetailView, NotificationListView

urlpatterns = [
    path("", NotificationListView.as_view(), name="notifications"),
    path('<uuid:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
]
