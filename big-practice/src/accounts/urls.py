from django.urls import path
from .views import LoginView, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    # Try to use sign-in and refresh token from rest_framework_simplejwt
    path("sign-in/", TokenObtainPairView.as_view(), name="user_sign_in"),
    path('refresh/', TokenRefreshView.as_view(),
         name='token_refresh')
]
