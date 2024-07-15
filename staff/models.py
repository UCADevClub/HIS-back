from django.db import models
from user_authentication.models import StandardUser, BaseUser


class Speciality(models.Model):
    position = models.CharField(unique=True, max_length=256)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.position
    
    class Meta:
        db_table = 'Speciality'


class Doctor(StandardUser):
    speciality = models.ManyToManyField(
        Speciality,
        related_name='doctors',
    )
    is_doctor = True
    is_branch_director = models.BooleanField(default=False)
    is_department_director = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name} {self.speciality}'
    
    class Meta:
        db_table = 'Doctor'


class PatientManager(StandardUser):
    is_staff = True
    is_patient_manager = True

    class Meta:
        db_table = 'PatientManager'


class BranchAdministrator(BaseUser):
    is_branch_administrator = True
    is_staff = True

    class Meta:
        db_table = 'BranchAdministrator'

class HospitalAdministrator(BaseUser):
    is_hospital_administrator = True
    is_staff = True

    class Meta:
        db_table = 'HospitalAdministrator'