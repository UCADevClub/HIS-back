from django.db import models
from patient.models import Patient


class Department(models.Model):
    department_name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.department_name


class Speciality(models.Model):
    position_name = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return self.position_name


class Doctor(Patient):

    speciality = models.OneToOneField(Speciality, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    is_head_of_department = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name} {self.speciality}'


class HumanResource(Patient):
    ...
