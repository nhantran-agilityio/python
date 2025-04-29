from django.urls import path
from .views import KinDetailAPIView

urlpatterns = [
    path('', KinDetailAPIView.as_view(), name='kin-detail'),
]
