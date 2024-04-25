from django.urls import path
from hospital.views import HospitalUpdateView, HospitalCreateView, HospitalListView


app_name = 'hospital'

urlpatterns = [
    # Hospital URLs
    path('create/', HospitalCreateView.as_view(), name='hospital-create'),
    path('<int:pk>/update/', HospitalUpdateView.as_view(), name='hospital-update'),
    path('hospital-list/', HospitalListView.as_view(), name='hospital-list'),
    
]