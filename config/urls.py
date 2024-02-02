from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/auth/', include('djoser.urls')),
    path('user/auth/', include('djoser.urls.authtoken')),
    path('patient/', include('patient.urls'))
]
