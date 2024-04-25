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
        fields = '__all__'


class BranchAdministratorSerializer(ModelSerializer):
    class Meta:
        model = BranchAdministrator
        fields = '__all__'


class HospitalAdministratorSerializer(ModelSerializer):
    class Meta:
        model = HospitalAdministrator
        fields = '__all__'


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
