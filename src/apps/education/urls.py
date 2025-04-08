from django.urls import path
from .views import EducationDetailAPIView

urlpatterns = [
    path('<uuid:user_id>/', EducationDetailAPIView.as_view(),
         name='education-by_user'),
]
