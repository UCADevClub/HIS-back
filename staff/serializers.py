from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from staff.models import (
    PatientManager,
    BranchAdministrator,
    HospitalAdministrator,
    Doctor,
    Speciality
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
        fields = ('id',)+ StandardUserSerializer.Meta.fields

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
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        primary_emergency_contact_data = validated_data.pop('primary_emergency_contact', None)
        secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact', None)

        if address_data:
            address_serializer = AddressSerializer(instance.address, data=address_data, partial=True)
            if address_serializer.is_valid(raise_exception=True):
                address_serializer.save()

        if primary_emergency_contact_data:
            primary_emergency_contact_serializer = EmergencyContactSerializer(instance.primary_emergency_contact, data=primary_emergency_contact_data, partial=True)
            if primary_emergency_contact_serializer.is_valid(raise_exception=True):
                primary_emergency_contact_serializer.save()

        if secondary_emergency_contact_data:
            if instance.secondary_emergency_contact:
                secondary_emergency_contact_serializer = EmergencyContactSerializer(instance.secondary_emergency_contact, data=secondary_emergency_contact_data, partial=True)
            else:
                secondary_emergency_contact_serializer = EmergencyContactSerializer(data=secondary_emergency_contact_data)
                
            if secondary_emergency_contact_serializer.is_valid(raise_exception=True):
                instance.secondary_emergency_contact = secondary_emergency_contact_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


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

        branch_administrator = BranchAdministrator.objects.create_branch_administrator(**validated_data)
        return branch_administrator
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


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
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class SpecialitySerializer(ModelSerializer):
    class Meta:
        model = Speciality
        fields = '__all__'

class DoctorSerializer(StandardUserSerializer):
    address = AddressSerializer()
    primary_emergency_contact = EmergencyContactSerializer()
    secondary_emergency_contact = EmergencyContactSerializer(required=False,allow_null = True)
    speciality = serializers.PrimaryKeyRelatedField(queryset = Speciality.objects.all(), many = True)

    class Meta(StandardUserSerializer.Meta):
        model = Doctor
        fields =('id',)+ StandardUserSerializer.Meta.fields + ('speciality','is_doctor','is_branch_director','is_department_director',)
       

    def create(self, validated_data):
        
        address_data = validated_data.pop('address')
        primary_emergency_contact_data = validated_data.pop('primary_emergency_contact', None)
        secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact', None)
        speciality_data = validated_data.pop('speciality')

        
        address = Address.objects.create(**address_data)
        primary_emergency_contact = EmergencyContact.objects.create(**primary_emergency_contact_data)
        secondary_emergency_contact = EmergencyContact.objects.create(**secondary_emergency_contact_data) if secondary_emergency_contact_data else None
        
        
        validated_data['address'] = address
        validated_data['primary_emergency_contact'] = primary_emergency_contact
        validated_data['secondary_emergency_contact'] = secondary_emergency_contact

        
        doctor = Doctor.objects.create_doctor(**validated_data)
        
        doctor.speciality.set(speciality_data)
        return doctor
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        primary_emergency_contact_data = validated_data.pop('primary_emergency_contact', None)
        secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact', None)
        speciality_data = validated_data.pop('speciality', None)

        if address_data:
            address_serializer = AddressSerializer(instance.address, data=address_data, partial=True)
            if address_serializer.is_valid(raise_exception=True):
                address_serializer.save()

        if primary_emergency_contact_data:
            primary_emergency_contact_serializer = EmergencyContactSerializer(
                instance.primary_emergency_contact, data=primary_emergency_contact_data, partial=True
            )
            if primary_emergency_contact_serializer.is_valid(raise_exception=True):
                primary_emergency_contact_serializer.save()

        if secondary_emergency_contact_data:
            if instance.secondary_emergency_contact:
                secondary_emergency_contact_serializer = EmergencyContactSerializer(
                    instance.secondary_emergency_contact, data=secondary_emergency_contact_data, partial=True
                )
            else:
                secondary_emergency_contact_serializer = EmergencyContactSerializer(data=secondary_emergency_contact_data)
            if secondary_emergency_contact_serializer.is_valid(raise_exception=True):
                instance.secondary_emergency_contact = secondary_emergency_contact_serializer.save()

        if speciality_data:
           
            specialities = Speciality.objects.filter(id__in=[spec.id for spec in speciality_data])
            
            instance.speciality.set(specialities)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance