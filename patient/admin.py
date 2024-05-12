from django.contrib import admin
from .models import Patient
from user_authentication.models import (
    EmergencyContact,
)

# Register your models here.
admin.site.register(EmergencyContact)
admin.site.register(Patient)
