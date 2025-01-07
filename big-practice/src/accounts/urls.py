from django.urls import path
# from .views import LoginView, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import LoginView, activate_account, RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    # path("register/", RegisterView.as_view(), name="register"),
    # Try to use sign-in and refresh token from rest_framework_simplejwt
    path("sign-in/", TokenObtainPairView.as_view(), name="user_sign_in"),
    path('refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    # path('register/', register, name='register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),

    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
