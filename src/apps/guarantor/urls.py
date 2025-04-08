from django.urls import path
from .views import GuarantorDetailAPIView

urlpatterns = [
    path('<uuid:user_id>/', GuarantorDetailAPIView.as_view(),
         name='guarantor-by-user'),
]
