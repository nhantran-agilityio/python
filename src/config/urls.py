from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from config.swagger import schema_view

API_ROOT = settings.API_ROOT_ENDPOINT


def api_path(route: str, view, *args, **kwargs):
    return path(f"{API_ROOT}{route}", view, *args, **kwargs)


apps_urls = [
    api_path("admin/", admin.site.urls),
    api_path("accounts/", include('accounts.urls')),
    api_path("jobs/", include('jobs.urls')),
    api_path("kins/", include('kins.urls')),
    api_path("documents/", include('documents.urls')),
    api_path("leave-applications/", include('leave_applications.urls')),
    api_path("guarantors/", include('guarantors.urls')),
    api_path("educations/", include('educations.urls')),
    api_path("families/", include('families.urls')),
    api_path("bank-accounts/", include('bank_accounts.urls')),
    api_path("notifications/", include('notifications.urls')),
    api_path("api-auth/", include('rest_framework.urls')),
    api_path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

swagger_urls = [
    api_path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    api_path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),
    api_path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name="schema-redoc"),
]

urlpatterns = apps_urls + swagger_urls

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
