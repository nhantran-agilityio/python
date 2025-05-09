from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.http import urlsafe_base64_decode
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from accounts.service import UserRegistrationService
from core.responses import ApiResponse
from utils.conversions import convert_request_data_keys_to_snake_and_flat_nested
from .serializers import LoginSerializer
from .models import User
from .serializers import (
    RegisterSerializer,
    UserDetailSerializer,
    UserListSerializer,
)


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

        """
        Register a new user.

        This endpoint takes a User object as input and saves it in the database.
        The password is hashed and the user's email is set to unverified.
        The user is then sent a verification email to the email address provided.

        :param request: The request object
        :type request: Request
        :return: The response object
        :type: Response
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserRegistrationService.register_user(serializer)

        return ApiResponse(
            message="User registered successfully. Please check your email to activate your account.",
            status_code=status.HTTP_201_CREATED
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def activate_account(request, uidb64, token):
    """
    Activate a user account.

    This endpoint receives a base64-encoded user ID and a token, decodes the user ID,
    and checks the validity of the token. If valid, the user's account is activated.

    :param request: The request object
    :type request: django.http.HttpRequest
    :param uidb64: Base64 encoded user ID
    :type uidb64: str
    :param token: Token to verify the user's identity
    :type token: str
    :return: ApiResponse indicating success or failure of account activation
    :type: core.responses.ApiResponse
    :raises ValidationError: If the token is invalid or expired
    """

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return ApiResponse(
            message="Account activated successfully.",
            status_code=status.HTTP_200_OK
        )
    else:
        raise ValidationError({"error": "Invalid or expired token."})


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Login a user.

        This endpoint takes a User object as input and verifies the username and password.
        If valid, a refresh and access token are generated and returned.

        :param request: The request object
        :type request: Request
        :raises AuthenticationFailed: If the credentials are invalid
        :return: ApiResponse containing the refresh and access token, as well as the user data
        :type: core.responses.ApiResponse
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self._authenticate_user(serializer.validated_data)
        if not user:
            raise AuthenticationFailed("Invalid credentials")

        tokens = self._generate_tokens(user)
        return ApiResponse(
            data={
                **tokens,
                "user": self._get_user_data(user)
            },
            status_code=status.HTTP_200_OK
        )

    def _authenticate_user(self, validated_data):
        """
        Authenticates a user based on the given validated data.

        :param validated_data: Data that has been validated by a serializer
        :type validated_data: dict
        :return: The authenticated user
        :type: django.contrib.auth.models.User
        :raises AuthenticationFailed: If the credentials are invalid
        """
        return authenticate(
            request=self.request,
            username=validated_data["email"],
            password=validated_data["password"]
        )

    def _generate_tokens(self, user):
        """
        Generates a refresh and access token for the given user.

        :param user: The user to generate the tokens for
        :type user: django.contrib.auth.models.User
        :return: A dictionary containing the refresh and access token
        :type: dict
        """
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    def _get_user_data(self, user):
        """
        Returns a dictionary containing user data.

        The returned dictionary contains the user's ID, email, role, and username.

        :param user: The user to generate the data for
        :type user: django.contrib.auth.models.User
        :return: A dictionary containing the user's data
        :type: dict
        """
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "username": user.get_full_name()
        }


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    # Required for file uploads
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """
        Retrieves the current user's profile.

        :param request: The request object
        :type request: django.http.HttpRequest
        :return: ApiResponse containing the user's data
        :type: core.responses.ApiResponse
        """
        user = User.objects.select_related('job').prefetch_related(
            'job__responsibilities').get(id=request.user.id)
        serializer = UserDetailSerializer(user)
        return ApiResponse(
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Update current user's profile (supports camelCase, nested job/contact/kin, avatar upload)",
        manual_parameters=[
            openapi.Parameter('firstName', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('lastName', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('phone', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('avatar', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('residentialAddress', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('cityOfResidence', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('phoneNum2', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter(
                'job',
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description='Stringified JSON. Example: {"department": "IT", "title": "Engineer"}'
            ),
            openapi.Parameter(
                'kin',
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description=(
                    'Stringified JSON. Example: {"fullName": "Bob", '
                    '"relationship": "Brother"}'
                )
            ),
        ],
        responses={200: UserDetailSerializer}
    )
    def patch(self, request):
        # Convert camelCase & parse nested JSON fields
        # Ensure the user instance is fetched with related fields for nested
        # updates
        """
        Partially updates the current user's profile.

        This method supports updates to the user's basic information as well as nested
        structures for job and kin details. The request data can be in camelCase, and
        nested JSON fields for 'job', 'contact', and 'kin' are parsed and converted to
        the appropriate format. The user profile is updated based on the provided data,
        and a refreshed user object is returned upon successful update.

        :param request: The HTTP request object containing user data
        :type request: django.http.HttpRequest
        :return: Response containing the updated user data
        :rtype: rest_framework.response.Response
        :raises ValidationError: If the provided data is invalid
        """

        convert_request_data_keys_to_snake_and_flat_nested(
            request,
            json_fields=["job", "contact", "kin"]
        )

        User.objects.select_related('job').prefetch_related(
            'job__responsibilities').get(id=request.user.id)
        serializer = UserDetailSerializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.user.refresh_from_db()
        return Response(UserDetailSerializer(request.user).data)


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    queryset = User.objects.all()
    serializer_class = UserListSerializer
