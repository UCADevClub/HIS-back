from django.contrib import admin
from .models import EmergencyContact, Patient

# Register your models here.
admin.site.register(EmergencyContact)
admin.site.register(Patient)
