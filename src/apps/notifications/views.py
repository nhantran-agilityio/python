from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=
        "Retrieve a list of unread notifications for the authenticated user.",
        responses={200: NotificationSerializer(many=True)}
    )
    def get(self, request):
        """
        Retrieve a list of unread notifications for the authenticated user.
        """
        notifications = Notification.objects.filter(user=request.user,
                                                    is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description=
        "Mark a notification as read or create a new notification.",
        request_body=NotificationSerializer,
        responses={
            201: NotificationSerializer,
            400: "Invalid data provided.",
        }
    )
    def post(self, request):
        """
        Mark a notification as read or create a new notification.
        """
        data = request.data.copy()
        data["user"] = request.user.id
        data["is_read"] = True
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
