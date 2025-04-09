from django.shortcuts import get_object_or_404
from apps.accounts.models import User
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Education
from .serializers import EducationSerializer


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_id = self.request.query_params.get("user_id")
        record_type = self.request.query_params.get("type")  # Optional

        queryset = self.queryset

        if user_id:
            queryset = queryset.filter(user__id=user_id)
        else:
            queryset = queryset.filter(user=user)

        # Only filter by type if user passes it
        if record_type in ["Academic", "Professional"]:
            queryset = queryset.filter(type=record_type)

        return queryset

    def perform_create(self, serializer):
        user_id = self.request.query_params.get("user_id")
        if user_id:
            user = get_object_or_404(User, id=user_id)

            if not self.request.user.is_staff and user != self.request.user:
                raise PermissionDenied("You are not allowed to create record for this user.")

            serializer.save(user=user)
        else:
            # Default to current user logged in
            serializer.save(user=self.request.user)
