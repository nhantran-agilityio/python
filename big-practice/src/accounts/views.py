from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer, LoginSerializer
from .models import User


class RegisterView(generics.CreateAPIView):
    """
    The API View for user registration
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    """
    The API View for user login.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handles the HTTP POST request for user login
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
