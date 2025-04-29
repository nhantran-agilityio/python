from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import FinancialViewSet

router = DefaultRouter()
router.register('', FinancialViewSet, basename='financial')

urlpatterns = [
    path('', include(router.urls)),
]
