from django.urls import path
from .views import (
    RegisterView,
    activate_account,
    LoginView,
    UserDetailView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/<str:pk>/', UserDetailView.as_view(), name='user-detail'),
]
