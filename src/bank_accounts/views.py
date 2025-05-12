from django.forms import ValidationError
from core.api_views import BaseAuthenticatedModelViewSet
from .models import BankAccount
from .serializers import BankAccountSerializer


class BankAccountViewSet(BaseAuthenticatedModelViewSet):
    serializer_class = BankAccountSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return BankAccount.objects.none()
        return BankAccount.objects.filter(user=user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated to create a BankAccount.")
        serializer.save(user=self.request.user)
