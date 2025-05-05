from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


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


urlpatterns = [
    path(f"{settings.API_ROOT_ENDPOINT}admin/", admin.site.urls),
    path(f"{settings.API_ROOT_ENDPOINT}accounts/", include('accounts.urls')),
    path(
        f"{settings.API_ROOT_ENDPOINT}api-auth/",
        include("rest_framework.urls"),
    ),
    path(f"{settings.API_ROOT_ENDPOINT}api/token/refresh/",
         TokenRefreshView.as_view(), name='token_refresh'),
    path(f"{settings.API_ROOT_ENDPOINT}jobs/", include('jobs.urls')),
    path(f"{settings.API_ROOT_ENDPOINT}kins/", include('kin.urls')),
    path(f"{settings.API_ROOT_ENDPOINT}documents/", include('document.urls')),
    path(f"{settings.API_ROOT_ENDPOINT}leave-applications/",
         include('leave_application.urls')),
    path(f"{settings.API_ROOT_ENDPOINT}guarantors/", include('guarantor.urls')),
    path(f"{settings.API_ROOT_ENDPOINT}educations/", include('education.urls')),
    path(f"{settings.API_ROOT_ENDPOINT}families/", include('family.urls')),
    path(f"{settings.API_ROOT_ENDPOINT}bank-account/", include('bank_account.urls')),


    # Swagger URLs
    path(
        f"{settings.API_ROOT_ENDPOINT}swagger.json",
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        f"{settings.API_ROOT_ENDPOINT}swagger/",
        schema_view.with_ui(
            'swagger',
            cache_timeout=0
        ),
        name='schema-swagger-ui',
    ),
    path(
        f"{settings.API_ROOT_ENDPOINT}redoc/",
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
