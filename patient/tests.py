from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from .models import EmergencyContact, Patient
from user_authentication.models import Address
from .serializers import EmergencyContactSerializer, PatientSerializer
from user_authentication.serializers import AddressSerializer
import json

class EmergencyContactTestCase(TestCase):
    def setUp(self):
        self.address = Address.objects.create(street="123 Main St", city="City", state="State", postal_code="12345")
        self.address_data = model_to_dict(self.address)
        print("Address: ", self.address_data)
        self.emergency_contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890",
            "address": self.address_data,  
        }

    def test_create_emergency_contact(self):
        response = self.client.post(reverse('patient:create-emergency-contact'), data=json.dumps(self.emergency_contact_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success", "contact_id": 1})


    def test_edit_emergency_contact(self):
        emergency_contact = EmergencyContact.objects.create(**self.emergency_contact_data)
        updated_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "phone_number": "9876543210",
            "address": self.address_data,
        }
        response = self.client.put(reverse('patient:edit-emergency-contact', args=[emergency_contact.id]), data=updated_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success", "contact_id": emergency_contact.id})


    def test_delete_emergency_contact(self):
        emergency_contact = EmergencyContact.objects.create(**self.emergency_contact_data)
        response = self.client.delete(reverse('patient:delete-emergency-contact', args=[emergency_contact.id]), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success"})


    def test_get_emergency_contact(self):
        emergency_contact = EmergencyContact.objects.create(**self.emergency_contact_data)
        response = self.client.get(reverse('patient:get-emergency-contact', args=[emergency_contact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), EmergencyContactSerializer(emergency_contact).data)

class PatientTestCase(TestCase):
    def setUp(self):
        self.address = Address.objects.create(street="123 Main St", city="City", state="State", postal_code="12345")
        self.address_data = model_to_dict(self.address)
        self.emergency_contact = EmergencyContact.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            address=self.address_data
        )
        self.patient_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "gender": "F",
            "date_of_birth": "1990-01-01",
            "primary_address": self.address_data,
            "primary_emergency_contact": self.emergency_contact,

        }

    def test_create_patient(self):
        response = self.client.post(reverse('patient:create-patient'), data=self.patient_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success", "patient_id": 1})

    def test_edit_patient(self):
        patient = Patient.objects.create(**self.patient_data)
        updated_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@example.com",
            "gender": "M",
            "date_of_birth": "1995-01-01",
            "primary_address": self.address_data,
            "primary_emergency_contact": self.emergency_contact,
        }
        response = self.client.put(reverse('patient:edit-patient', args=[patient.individual_unique_number]), data=updated_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success", "patient_id": patient.individual_unique_number})

    def test_get_patient(self):
        patient = Patient.objects.create(**self.patient_data)
        print(f"Patient ID: {patient.individual_unique_number}")  
        response = self.client.get(reverse('patient:get-patient', args=[patient.individual_unique_number]), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), PatientSerializer(patient).data)


    def test_delete_patient(self):
        patient = Patient.objects.create(**self.patient_data)
        response = self.client.delete(reverse('patient:delete-patient', args=[patient.individual_unique_number]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success"})



    def test_get_all_patients(self):
        Patient.objects.create(**self.patient_data)
        response = self.client.get(reverse('patient:get-all-patients'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
