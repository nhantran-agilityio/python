from rest_framework.routers import DefaultRouter
from .views import KinViewSet

router = DefaultRouter()
router.register('', KinViewSet, basename='kins')

urlpatterns = router.urls
