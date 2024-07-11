from django.db import models
from staff.models import (
    Doctor,
    BranchAdministrator,
    HospitalAdministrator,
    PatientManager,
)


class BranchPhoneNumber(models.Model):
    phone_number = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.phone_number}'
    
    class Meta:
        db_table = 'BranchPhoneNumber'


class BranchAddress(models.Model):
    street_address = models.CharField(max_length=255)
    building_number = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=32)
    country = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.street_address}, {self.building_number}, {self.city}, {self.country}"
    
    class Meta:
        db_table = 'BranchAddress'

class Hospital(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    hospital_administrator = models.OneToOneField(
        HospitalAdministrator,
        on_delete=models.CASCADE,
        related_name='hospital',
    )

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = 'Hospital'


class Branch(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.OneToOneField(
        BranchAddress,
        on_delete=models.CASCADE,
        related_name='branch',
    )
    phone_numbers = models.ManyToManyField(
        BranchPhoneNumber,
        related_name='branch',
    )
    director = models.OneToOneField(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='branch',
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name='branches',
    )
    doctors = models.ManyToManyField(
        Doctor,
        related_name='doctors',
    )
    branch_administrator = models.OneToOneField(
        BranchAdministrator,
        on_delete=models.SET_NULL,
        null=True,
        related_name='branch',
    )
    patient_manager = models.ForeignKey(
        PatientManager,
        on_delete=models.SET_NULL,
        null=True,
        related_name='patient_manager',
    )

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = 'Branch'


class Department(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    head = models.OneToOneField(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='department_head',
    )
    branches = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='branches',
    )

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = 'Department'
    

class Allergy(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    symptoms = models.TextField()
    diagnostic_method = models.TextField()
    treatment_method = models.TextField()
    types = models.CharField()
    restrictions = models.TextField()

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = 'Allergy'


class Vaccine(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    contraindications = models.TextField()
    reaction = models.TextField()
    composition = models.TextField()
    diseases_prevention = models.TextField()
    symptoms = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Vaccine'


class Pill(models.Model):
    name = models.CharField(max_length=128, unique=True)
    purpose = models.TextField()
    composition = models.TextField()
    indications = models.TextField()
    contraindications = models.TextField()
    side_effects = models.TextField()
    special_instructions = models.TextField()
    dosage_and_administration = models.TextField()
    storage_conditions = models.TextField()
    expiry_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Pill'