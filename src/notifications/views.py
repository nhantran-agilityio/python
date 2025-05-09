from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from core.utilities import is_admin
from notifications.models import Notification

from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    resource_name = "notification"

    @swagger_auto_schema(
        operation_description="List all notifications. Admin sees all, users see only theirs.",
        responses={200: NotificationSerializer(many=True)}
    )
    def list(self, request):
        if is_admin(request):
            notifications = Notification.objects.filter(is_read=False)
        else:
            notifications = Notification.objects.filter(user=request.user, is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new notification for the authenticated user.",
        request_body=NotificationSerializer,
        responses={201: NotificationSerializer, 400: "Invalid data"}
    )
    def create(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = NotificationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Retrieve a specific notification by ID. Returns empty if not found or unauthorized.",
        responses={200: NotificationSerializer}
    )
    def retrieve(self, request, pk=None):
        notification = self.get_notification(pk, request)
        if not notification:
            return Response({}, status=status.HTTP_200_OK)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Partially update a notification (e.g. mark as read).",
        request_body=NotificationSerializer,
        responses={200: NotificationSerializer, 400: "Invalid data"}
    )
    def partial_update(self, request, pk=None):
        notification = self.get_notification(pk, request)
        if not notification:
            return Response({}, status=status.HTTP_200_OK)
        serializer = NotificationSerializer(notification, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Delete a notification by ID.",
        responses={204: "Deleted successfully", 404: "Not found"}
    )
    def destroy(self, request, pk=None):
        notification = self.get_notification(pk, request)
        if not notification:
            return Response({}, status=status.HTTP_200_OK)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_notification(self, pk, request):
        """
        Helper to get notification by id and user.
        Admins can access all notifications.
        """
        if is_admin(request):
            return Notification.objects.filter(pk=pk).first()
        return Notification.objects.filter(pk=pk, user=request.user).first()


apps = [NotificationViewSet]
