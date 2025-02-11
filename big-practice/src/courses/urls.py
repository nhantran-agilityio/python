from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'statistics/', 
        views.CourseStatisticsView.as_view(), 
        name='course_statistics'
    ),
]
