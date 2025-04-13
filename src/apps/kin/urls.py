from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KinViewSet

router = DefaultRouter()
router.register(r'', KinViewSet, basename='kin')

urlpatterns = [
    path('', include(router.urls)),
]
