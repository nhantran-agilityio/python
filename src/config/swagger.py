from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Human Resource Management API",
        default_version='v1',
        description="API documentation for User Management System",
        terms_of_service="https://www.yoursite.com/terms/",
        contact=openapi.Contact(email="contact@yoursite.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=[JWTAuthentication],
    permission_classes=[permissions.AllowAny],
)
