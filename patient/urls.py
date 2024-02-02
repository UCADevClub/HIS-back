from django.urls import path
from patient.views import PatientDetail, PatientList


app_name = 'patient'

urlpatterns = [
    # Patient URLs
    path('patient-detail/<int:inn>/', PatientDetail.as_view(), name='patient-detail'),
    path('patient-list/', PatientList.as_view(), name='patient-list'),
]
