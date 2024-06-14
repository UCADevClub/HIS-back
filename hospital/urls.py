from django.urls import path
from hospital.views import (
    HospitalUpdateView,
    HospitalCreateView,
    HospitalListView,
    BranchListCreateAPIView,
    BranchRetrieveUpdateAPIView,
    BranchView,
)


app_name = 'hospital'

urlpatterns = [
    # Hospital URLs
    path('create-hospital/', HospitalCreateView.as_view(), name='create-hospital'),
    path('list-hospital/',HospitalListView.as_view(), name='list-hospital'),
    path('update-hospital/<int:pk>', HospitalUpdateView.as_view(), name='update-hospital'),

    # Branch URLs
    path('view-branch/<int:pk>', BranchRetrieveUpdateAPIView.as_view(), name='view-branch'),
    path('create-branch/', BranchView.as_view(), name='create-branch'),
    # path('view-branch/<int:pk>', BranchView.as_view(), name='view-branch'),
    path('list-branch/', BranchListCreateAPIView.as_view(), name='list-branch'),
    

    
]