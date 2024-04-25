from rest_framework.serializers import ModelSerializer
from staff.models import (
    PatientManager,
    BranchAdministrator,
    HospitalAdministrator,
    Doctor,
)


class PatientManagerSerializer(ModelSerializer):
    class Meta:
        model = PatientManager
        exclude = ['password']


class BranchAdministratorSerializer(ModelSerializer):
    class Meta:
        model = BranchAdministrator
        exclude = ['password']


class HospitalAdministratorSerializer(ModelSerializer):
    class Meta:
        model = HospitalAdministrator
        exclude = ['password']


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ['password']
