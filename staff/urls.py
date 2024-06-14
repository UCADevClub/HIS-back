from django.urls import path
from staff.views import (
    HospitalAdministratorSingleView,
    HospitalAdministratorView,
    BranchAdministratorView,
    DoctorCreateView,
    PatientManagerCreateView
)

app_name = 'staff'

urlpatterns = [
    path('view-hospital-administrator/<int:pk>', HospitalAdministratorSingleView.as_view(), name='hospital-administrator-single'),
    path('create-hospital-administrator', HospitalAdministratorView.as_view(), name='hospital-administrator'),
    path('create-branch-administrator', BranchAdministratorView.as_view(), name='branch-administrator'),
    path('create-doctor',DoctorCreateView.as_view(),name='create-doctor' ),
    path('create-patient-manager',PatientManagerCreateView.as_view(), name='create-patient-manager')
]
