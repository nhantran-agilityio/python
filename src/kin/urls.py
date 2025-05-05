from django.urls import path

from kin.views import KinDetailAPIView

urlpatterns = [
    path('', KinDetailAPIView.as_view(), name='kin-detail'),
]
