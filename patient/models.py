from django.db import models
from user_authentication.models import BaseUser, Address


class EmergencyContact(models.Model):
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=32)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='emergency_contacts')

    def __str__(self):
        return f"Emergency Contact: {self.first_name} {self.last_name}"


class Patient(BaseUser):
    MARITAL_OPTIONS = (
            ('single', 'Single'),
            ('married', 'Married'),
            ('widowed', 'Widowed'),
            ('separated', 'Separated'),
            ('divorced', 'Divorced'),
            ('common_law', 'Common-Law')
    )

    marital_status = models.CharField(max_length=64, choices=MARITAL_OPTIONS, default='single')
    primary_emergency_contact = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE, related_name='primary_emergency_contact')
    secondary_emergency_contact = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE, related_name='secondary_emergency_contact', blank=True)

    def __str__(self):
        return f"Patient: {self.first_name} {self.last_name}"
