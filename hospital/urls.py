from django.urls import path
from hospital.views import (
    HospitalUpdateView,
    HospitalCreateView,
    HospitalListView,
    BranchListAPIView,
    BranchRetrieveUpdateAPIView,
    BranchCreateView,
    BranchUpdateView,
    AllergyCreateView,
    AllergyListView,
    AllergyRetrieveUpdateDelete,
    VaccineCreateView,
    VaccineListView,
    VaccineRetrieveUpdateDelete,
    PillCreateView,
    PillListView,
    PillRetrieveUpdateDelete
)


app_name = 'hospital'

urlpatterns = [
    # Hospital URLs
    path('create-hospital/', HospitalCreateView.as_view(), name='create-hospital'),
    path('list-hospital/',HospitalListView.as_view(), name='list-hospital'),
    path('update-hospital/<int:pk>', HospitalUpdateView.as_view(), name='update-hospital'),

    # Branch URLs
    path('view-branch/<int:pk>', BranchRetrieveUpdateAPIView.as_view(), name='view-branch'),
    path('create-branch/', BranchCreateView.as_view(), name='create-branch'),
    path('list-branch/', BranchListAPIView.as_view(), name='list-branch'),
    path('update-branch/<int:pk>', BranchUpdateView.as_view(), name='update-branch'),

    #Allergy URLs
    path('create-allergy', AllergyCreateView.as_view(), name='create-allergy'),
    path('list-allergies', AllergyListView.as_view(), name='list-allergies'),
    path('view-allergy/<int:pk>', AllergyRetrieveUpdateDelete.as_view(), name='view-allergy'),

    #Vaccine URLs
    path('create-vaccine', VaccineCreateView.as_view(), name= 'create-vaccine'),
    path('list-vaccines',VaccineListView.as_view(),name='list-vaccines'),
    path('view-vaccine/<int:pk>', VaccineRetrieveUpdateDelete.as_view(), name='view-vaccine'),

    #Pill URLs
    path('create-pill', PillCreateView.as_view(), name= 'create-pill'),
    path('list-pills', PillListView.as_view(), name='list-pills'),
    path('view-pill/<int:pk>', PillRetrieveUpdateDelete.as_view(), name='view-pill')
    
]