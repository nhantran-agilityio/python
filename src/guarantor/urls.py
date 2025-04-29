from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import GuarantorViewSet

router = DefaultRouter()
router.register('', GuarantorViewSet, basename='guarantor')

urlpatterns = [
    path('', include(router.urls)),
]
