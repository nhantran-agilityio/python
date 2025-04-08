from django.urls import path
from .views import FamilyDetailAPIView

urlpatterns = [
    path('<uuid:user_id>/', FamilyDetailAPIView.as_view(), name='family-by_user'),
]
