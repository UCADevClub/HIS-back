from django.db import models
from user_authentication.models import BaseUser


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.postal_code}"


class EmergencyContact(models.Model):
    patient: BaseUser = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='emergency_contacts')
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=32)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='emergency_contacts')

    def __str__(self):
        return f"Emergency Contact: {self.first_name} {self.last_name} for {self.patient.first_name} {self.patient.last_name}"


class Patient(BaseUser):
    address_1 = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_1', null=True)
    emergency_contact_1 = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE,
                                            related_name='emergency_contact_1', null=True)
    emergency_contact_2 = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE,
                                            related_name='emergency_contact_2', null=True)

    def __str__(self):
        return f"Patient: {self.first_name} {self.last_name}"