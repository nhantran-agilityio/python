import os
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserDetailSerializer, UserListSerializer
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes,  force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from urllib.parse import urlencode
from .serializers import LoginSerializer
from dotenv import load_dotenv
from .models import User


load_dotenv()


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        operation_description="Register a new user",
        responses={
            status.HTTP_201_CREATED: "User registered successfully",
            status.HTTP_400_BAD_REQUEST: "Bad Request - Invalid Data"
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            mail_subject = 'Activate your account.'
            frontend_url = os.getenv("FE_DOMAIN")
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            params = {
                "uidb64": uid,
                "token": token
            }
            activation_link = f"{frontend_url}?{urlencode(params)}"
            message = render_to_string('email/activation_email.txt', {
                'user': user,
                'domain': activation_link,
            })
            to_email = user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return Response(
                {
                    "message": "User registered successfully. "
                               "Please check your email to activate your account."
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate or retrieve the token for the user
            token, created = Token.objects.get_or_create(user=user)

            # Return the token and user info
            return Response({
                "token": token.key,
                "user_id": user.id,
                "email": user.email
            }, status=status.HTTP_200_OK)

        # Return errors if invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={

            }
        ),
        responses={200: 'User updated successfully'}
    )
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)

        if request.user != user:
            return Response(
                {"error": "You do not have permission to edit this user."},
                status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
