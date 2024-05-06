from rest_framework.serializers import ModelSerializer
from django.contrib.auth import hashers
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
        fields = (
            'user_id',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'is_staff',
            'is_hospital_administrator'
        )

    def create(self, validated_data):
        """
        Creates a new HospitalAdministrator instance with hashed password.
        """

        hospital_administrator = HospitalAdministrator.objects.create_hospital_administrator(**validated_data)
        return hospital_administrator


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ['password']
