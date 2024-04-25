from django.contrib import admin
from .models import Doctor, BranchAdministrator, HospitalAdministrator, PatientManager, Speciality

admin.site.register(Doctor)
admin.site.register(BranchAdministrator)
admin.site.register(HospitalAdministrator)
admin.site.register(PatientManager)
admin.site.register(Speciality)