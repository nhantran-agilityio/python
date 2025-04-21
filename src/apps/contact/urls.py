from django.urls import path
from .views import (
    ContactDetailAPIView,
)

urlpatterns = [
    path('', ContactDetailAPIView.as_view(), name='contact-detail'),

]
