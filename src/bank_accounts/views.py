from core.api_views import BaseAuthenticatedModelViewSet
from core.custom_permissions import IsAdminOrOwner
from .models import BankAccount
from .serializers import BankAccountSerializer


class BankAccountViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return BankAccount.objects.visible_to(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
