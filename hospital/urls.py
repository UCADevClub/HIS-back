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
    # path('create-branch/', BranchListCreateAPIView.as_view(), name='create-branch'),
    path('view-brach/', BranchRetrieveUpdateAPIView.as_view(), name='view-branch'),
    path('create-branch', BranchView.as_view(), name='create-branch'),
    path('view-branch/<int:pk>', BranchView.as_view(), name='view-branch'),
    # path('<int:pk>/update/', HospitalUpdateView.as_view(), name='hospital-update'),
    # path('hospital-list/', HospitalListView.as_view(), name='hospital-list'),
    
]