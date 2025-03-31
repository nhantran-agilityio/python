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
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/jobs/', include('apps.job.urls')),
    path('api/documents/', include('apps.document.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/leave-applications/', include('apps.leave_application.urls')),

    # Swagger URLs
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
