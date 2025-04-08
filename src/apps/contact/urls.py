from django.urls import path

from apps.contact.views import ContactDetailAPIView


urlpatterns = [
    path('<uuid:user_id>/', ContactDetailAPIView.as_view(), name='contact-by-user'),
]
