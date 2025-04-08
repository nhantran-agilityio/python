from django.urls import path
from .views import KinDetailAPIView

urlpatterns = [
    path('<uuid:user_id>/', KinDetailAPIView.as_view(), name='kin-by_user'),
]
