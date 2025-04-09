from rest_framework.routers import DefaultRouter
from .views import EducationViewSet

router = DefaultRouter()
router.register(r'', EducationViewSet, basename='educations')

urlpatterns = router.urls
