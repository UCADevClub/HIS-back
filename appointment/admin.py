from django.contrib import admin
from .models import Appointment, ReferralAppointment

admin.site.register(Appointment)
admin.site.register(ReferralAppointment)