from django.urls import path
from .views import (
    RegisterView,
    UserListView,
    activate_account,
    LoginView,
    UserDetailView,
)

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserDetailView.as_view(), name='personal-info'),
]
