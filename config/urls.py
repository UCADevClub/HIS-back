from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_auth/', include('rest_framework.urls')),
    path('user_authentication/auth/', include('djoser.urls')),
    path('user_authentication/auth/', include('djoser.urls.authtoken')),
    path('user_authentication/auth/', include('djoser.urls.jwt')),
    path('patient/', include('patient.urls'))
]
