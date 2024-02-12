from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="HIS API",
      default_version='v1',
      description="API for Hospital Information System",
      terms_of_service="https://www.google.com/policies/terms/", # TODO: Change this
      contact=openapi.Contact(email="contact@snippets.local"), # TODO: Change this
      license=openapi.License(name="BSD License"), # TODO: Change this
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    # Swagger API documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('user/auth/', include('djoser.urls')),
    path('user/auth/', include('djoser.urls.authtoken')),
    path('patient/', include('patient.urls'))
]
