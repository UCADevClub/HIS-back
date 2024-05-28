from rest_framework.serializers import ModelSerializer
from staff.models import (
    PatientManager,
    BranchAdministrator,
    HospitalAdministrator,
    Doctor,
)
from user_authentication.models import (
    Address,
    EmergencyContact,
)
from user_authentication.serializers import (
    StandardUserSerializer,
    AddressSerializer,
    EmergencyContactSerializer,
)


class PatientManagerSerializer(StandardUserSerializer):
    address = AddressSerializer()
    primary_emergency_contact = EmergencyContactSerializer()
    secondary_emergency_contact = EmergencyContactSerializer(required=False)

    class Meta(StandardUserSerializer.Meta):
        model = PatientManager
        fields = StandardUserSerializer.Meta.fields

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        primary_emergency_contact_data = validated_data.pop('primary_emergency_contact', None)
        secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact', None)

        address = Address.objects.create(**address_data)
        primary_emergency_contact = EmergencyContact.objects.create(**primary_emergency_contact_data)
        if secondary_emergency_contact_data:
            secondary_emergency_contact = EmergencyContact.objects.create(**secondary_emergency_contact_data)
        else:
            secondary_emergency_contact = None

        validated_data['address'] = address
        validated_data['primary_emergency_contact'] = primary_emergency_contact
        validated_data['secondary_emergency_contact'] = secondary_emergency_contact

        return PatientManager.objects.create_patient_manager(**validated_data)


class BranchAdministratorSerializer(ModelSerializer):
    class Meta:
        model = BranchAdministrator
        fields = (
            'user_id',
            'first_name',
            'middle_name',
            'last_name',
            'email',
        )

    def create(self, validated_data):
        """
        Creates a new BranchAdministrator instance with hashed password.
        """

        hospital_administrator = HospitalAdministrator.objects.create_hospital_administrator(**validated_data)
        return hospital_administrator


class HospitalAdministratorSerializer(ModelSerializer):
    class Meta:
        model = HospitalAdministrator
        fields = (
            'user_id',
            'first_name',
            'middle_name',
            'last_name',
            'email',
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
