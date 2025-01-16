from django.urls import path
from .views import (
    InstructorCreateView,
    InstructorUpdateView,
    InstructorDeleteView
)

urlpatterns = [
    path(
        'instructors/create/',
        InstructorCreateView.as_view(),
        name='instructor-create'
    ),
    path(
        'instructors/update/<int:pk>/',
        InstructorUpdateView.as_view(),
        name='instructor-update'
    ),
    path(
        'instructors/delete/<int:pk>/',
        InstructorDeleteView.as_view(),
        name='instructor-delete'
    ),
]
