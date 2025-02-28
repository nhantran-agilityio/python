from django.urls import path, include
from .views import CourseViewSet, CourseStatisticsView, course_list
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'statistics/',
        CourseStatisticsView.as_view(),
        name='course_statistics'
    ),
    path('course-list/', course_list, name='course_list'),
]
