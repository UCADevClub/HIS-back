from django.urls import path
from .views import (
    EmergencyContactList,
    EmergencyContactDetail,
    PatientList,
    PatientDetail
)

app_name = 'patient'

urlpatterns = [
    # Emergency Contact URLs
    path('emergency-contacts/', EmergencyContactList.as_view(), name='emergency-contact-list'),
    path('emergency-contacts/<int:pk>/', EmergencyContactDetail.as_view(), name='emergency-contact-detail'),
    # Patient URLs
    path('', PatientList.as_view(), name='patient-list'),
    path('<int:pk>/', PatientDetail.as_view(), name='patient-detail'),
]
