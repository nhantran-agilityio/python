from core.api_views import BaseModelViewSet
from core.custom_permissions import IsAdminOrOwner
from core.mixins import CustomRetrieveModelMixin, CustomUpdateModelMixin
from .models import Notification
from .serializers import NotificationSerializer


class NotificationsViewSet(
    CustomRetrieveModelMixin,
    CustomUpdateModelMixin,
    BaseModelViewSet,
):
    serializer_class = NotificationSerializer
    http_method_names = ["get", "patch"]
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return Notification.objects.visible_to(user=self.request.user)
