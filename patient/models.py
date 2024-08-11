from django.db import models
from hospital.models import Allergy, Vaccine
from user_authentication.models import StandardUser

class Patient(StandardUser):
    blood_group = models.CharField(max_length=3, default='UNK')
    vision = models.CharField(max_length=50, default='UNK')
    allergies = models.ManyToManyField(Allergy, related_name='patients')
    vaccines = models.ManyToManyField(Vaccine, related_name='patients')
    
    is_patient = True

    class Meta:
        db_table = 'Patient'
        