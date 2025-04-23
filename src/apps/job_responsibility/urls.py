from rest_framework.routers import DefaultRouter
from .views import JobResponsibilityViewSet

router = DefaultRouter()
router.register('', JobResponsibilityViewSet, basename='jobs')

urlpatterns = router.urls
