from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, report_list
router = DefaultRouter()

router.register(r'reports', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('report-list/', report_list, name='report_list'),

]
