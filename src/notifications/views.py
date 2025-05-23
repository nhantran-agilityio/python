from core.api_views import BaseAuthenticatedModelViewSet
from core.custom_permissions import IsAdminOrOwner
from .models import Notification
from .serializers import NotificationSerializer


class NotificationsViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return Notification.objects.visible_to(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
