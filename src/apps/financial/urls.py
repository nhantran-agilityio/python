from django.urls import path
from .views import FinancialDetailAPIView

urlpatterns = [
    path('<uuid:user_id>/', FinancialDetailAPIView.as_view(),
         name='financial-by_user'),
]
