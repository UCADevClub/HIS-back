from django.urls import path
from user_authentication.views import TokenObtainView


urlpatterns = [
    path('login', TokenObtainView.as_view(), name='login'),
]
