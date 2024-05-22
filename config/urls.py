from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="HIS API",
      default_version='v1',
      description="API for Hospital Information System",
      terms_of_service="https://www.google.com/policies/terms/",  # TODO: Change this
      contact=openapi.Contact(email="contact@snippets.local"),  # TODO: Change this
      license=openapi.License(name="BSD License")  # TODO: Change this
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    # Swagger API documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api_auth/', include('rest_framework.urls')),
    path('user_authentication/auth/', include('djoser.urls')),
    path('user_authentication/auth/', include('djoser.urls.authtoken')),
    path('user_authentication/auth/', include('djoser.urls.jwt')),
    path('user_authentication/', include('user_authentication.urls')),
    path('patient/', include('patient.urls')),

    path('staff/', include('staff.urls')),

    # hospital
    path('hospital/', include('hospital.urls')),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
