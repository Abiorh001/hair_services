from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Hair Service API",
        default_version='v1',
        description="Hair Services API Documentation",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="Hair Services License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


api_version = 'v1'

urlpatterns = [
    path(f'api/{api_version}/admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(f'api/{api_version}/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(f'api/{api_version}/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path(f'api/{api_version}/', include('accounts.urls')),
    path(f'api/{api_version}/', include('professional_service_provider.urls')),
    path(f'api/{api_version}/', include('service_categories.urls')),
    path(f'api/{api_version}/', include('services.urls')),
    path(f'api/{api_version}/', include('appointment_booking.urls')),
    path(f'api/{api_version}/', include('review_and_rating.urls')),
    path(f'api/{api_version}/', include('products.urls')),
    path(f'api/{api_version}/', include('admin_user.urls')),
    path(f'api/{api_version}/', include('payment.urls')),
    
]
