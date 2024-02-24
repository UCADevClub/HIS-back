from django.urls import path
from patient.views import PatientDetail, PatientList, PatientCreateSet


app_name = 'patient'

urlpatterns = [
    # Patient URLs
    path('create/', PatientCreateSet.as_view(), name='patient-create'),
    path('patient-detail/<int:inn>/', PatientDetail.as_view(), name='patient-detail'),
    path('patient-list/', PatientList.as_view(), name='patient-list'),
]
