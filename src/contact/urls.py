from rest_framework.routers import DefaultRouter

from contact.views import ContactViewSet

router = DefaultRouter()
router.register('', ContactViewSet, basename='contacts')

urlpatterns = router.urls
