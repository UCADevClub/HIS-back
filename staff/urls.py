from django.urls import path
from staff.views import (
    HospitalAdministratorSingleView,
    HospitalAdministratorView,
    BranchAdministratorView,
    DoctorCreateView,
    DoctorListView,
    RetrieveUpdateDeleteDoctor,
    DoctorSearch,
    PatientManagerCreateView,
    PatientManagerListView,
    PatientManagerRetrieveUpdateDelete,
    SpecialityCreateAPIView

)

app_name = 'staff'

urlpatterns = [
    path('view-hospital-administrator/<int:pk>', HospitalAdministratorSingleView.as_view(), name='hospital-administrator-single'),
    path('create-hospital-administrator', HospitalAdministratorView.as_view(), name='hospital-administrator'),
    path('create-branch-administrator', BranchAdministratorView.as_view(), name='branch-administrator'),
    #Doctor URLs
    path('create-doctor',DoctorCreateView.as_view(),name='create-doctor' ),
    path("list-doctors", DoctorListView.as_view(), name='list-doctors' ),
    path('view-doctor/<int:pk>',RetrieveUpdateDeleteDoctor.as_view(), name='view-doctor'),
    path('search-doctor/', DoctorSearch.as_view(), name='doctor-search'),
    #Patient Manager URLs
    path('create-patient-manager',PatientManagerCreateView.as_view(), name='create-patient-manager'),
    path('list-patient-managers', PatientManagerListView.as_view(), name='list-patient-managers'),
    path('view-patient-manager/<int:pk>',PatientManagerRetrieveUpdateDelete.as_view(), name='view-patient-manager'),

    #Speciality URLs
    path('create-speciality', SpecialityCreateAPIView.as_view(), name='create-speciality'),
]
