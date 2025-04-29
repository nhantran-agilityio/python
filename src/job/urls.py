from rest_framework.routers import DefaultRouter
from .api.views import JobViewSet

router = DefaultRouter()
router.register('', JobViewSet, basename='jobs')

urlpatterns = router.urls
