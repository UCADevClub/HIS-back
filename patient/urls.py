from django.urls import path
from .views import (
    create_emergency_contact,
    edit_emergency_contact,
    delete_emergency_contact,
    get_emergency_contact,
    create_patient,
    edit_patient,
    delete_patient,
    get_patient,
    get_all_patients,
)

app_name = 'patient'

urlpatterns = [
    # Emergency Contact URLs
    path('create-emergency-contact/', create_emergency_contact, name='create-emergency-contact'),
    path('edit-emergency-contact/<int:contact_id>/', edit_emergency_contact, name='edit-emergency-contact'),
    path('delete-emergency-contact/<int:contact_id>/', delete_emergency_contact, name='delete-emergency-contact'),
    path('get-emergency-contact/<int:contact_id>/', get_emergency_contact, name='get-emergency-contact'),

    # Patient URLs
    path('create-patient/', create_patient, name='create-patient'),
    path('edit-patient/<int:patient_id>/', edit_patient, name='edit-patient'),
    path('delete-patient/<int:patient_id>/', delete_patient, name='delete-patient'),
    path('get-patient/<int:patient_id>/', get_patient, name='get-patient'),
    path('get-all-patients/', get_all_patients, name='get-all-patients'),
]
