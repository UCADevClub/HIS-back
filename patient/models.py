from django.db import models
from user_authentication.models import BaseUser, Address


class EmergencyContact(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=32)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='emergency_contacts')

    def __str__(self):
        return f"Emergency Contact: {self.first_name} {self.last_name}"


class Patient(BaseUser):
    primary_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='primary_address', null=True,
                                        blank=True)
    primary_emergency_contact = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE,
                                                  related_name='primary_emergency_contact', null=True, blank=True)
    secondary_emergency_contact = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE,
                                                    related_name='secondary_emergency_contact', null=True, blank=True)

    def __str__(self):
        return f"Patient: {self.first_name} {self.last_name}"
