from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'reports', views.ReportViewSet)

urlpatterns = [
    path('', include(router.urls))
]
