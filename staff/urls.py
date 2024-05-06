from django.urls import path
from staff.views import HospitalAdministratorSingleView, HospitalAdministratorView

app_name = 'staff'

urlpatterns = [
    path('hospital_administrator/<int:pk>', HospitalAdministratorSingleView.as_view(), name='hospital-administrator-single'),
    path('hospital_administrator', HospitalAdministratorView.as_view(), name='hospital-administrator'),
]
