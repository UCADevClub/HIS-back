from django.urls import path
from .views import (
    DoctorList,
    DoctorDetail
)

app_name = 'staff'
urlpatterns = [
    path('doctors/', DoctorList.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetail.as_view(), name='doctor-detail'),
]
