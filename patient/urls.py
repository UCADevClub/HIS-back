from django.urls import path
from patient.views import PatientDetail, PatientList, PatientCreateView, PatientSearch


app_name = 'patient'

urlpatterns = [
    # Patient URLs
    path('create/', PatientCreateView.as_view(), name='patient-create'),
    path('patient-detail/<str:user_id>/', PatientDetail.as_view(), name='patient-detail'),
    path('patient-list/', PatientList.as_view(), name='patient-list'),
    path('search/', PatientSearch.as_view(), name='search'),
]
