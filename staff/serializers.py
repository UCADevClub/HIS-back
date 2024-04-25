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
        exclude = ['password',]

    def create(self, validated_data):
        """
        Creates a new HospitalAdministrator instance with hashed password.
        """

        # Hash the password before saving
        validated_data['password'] = hashers.make_password(validated_data['password'])
        hospital_administrator = HospitalAdministrator.objects.create(**validated_data)
        return hospital_administrator
    
    def update(self, instance, validated_data):
        del validated_data['user_id']
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ['password']
