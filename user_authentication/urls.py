from django.urls import path
from user_authentication.views import TokenObtainView, LogoutView


urlpatterns = [
    path('login', TokenObtainView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
