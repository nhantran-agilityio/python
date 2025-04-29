from rest_framework.routers import DefaultRouter
from .api.views import EducationViewSet

router = DefaultRouter()
router.register('', EducationViewSet, basename='educations')

urlpatterns = router.urls
