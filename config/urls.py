from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/auth/', include('djoser.urls')),
    path('user/auth/', include('djoser.urls.authtoken')),
    path('api/v1/patient/', include('patient.urls')),
    path('api/v1/staff/', include('staff.urls')),
]
