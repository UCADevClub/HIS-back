from rest_framework import serializers
from .models import EmergencyContact, Patient
from user_authentication.serializers import BaseUserSerializer, AddressSerializer
from user_authentication.models import Address
from django.shortcuts import get_object_or_404

class EmergencyContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    def create(self, validated_data):
        validated_data['address'] = get_or_create(validated_data.pop('address'), Address)
        return super(PatientSerializer, self).create(validated_data)

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = EmergencyContact
        fields = '__all__'


class PatientSerializer(BaseUserSerializer):
    primary_address = AddressSerializer()
    primary_emergency_contact = EmergencyContactSerializer()
    secondary_emergency_contact = EmergencyContactSerializer()

    def create(self, validated_data):
        validated_data['primary_address'] = get_or_create(validated_data.pop('primary_address'), Address)
        validated_data['primary_emergency_contact'] = get_or_create(validated_data.pop('primary_emergency_contact'), EmergencyContact)
        validated_data['secondary_emergency_contact'] = get_or_create(validated_data.pop('secondary_emergency_contact'), EmergencyContact)
        return super(PatientSerializer, self).create(validated_data)


    def update(self, instance, validated_data):
        if validated_data.get('primary_address'):
            validated_data['primary_address'] = get_or_create(validated_data.pop('primary_address'), Address)
        if validated_data.get('primary_emergency_contact'):
            validated_data['primary_emergency_contact'] = get_or_create(validated_data.pop('primary_emergency_contact'), EmergencyContact)
        if validated_data.get('secondary_emergency_contact'):
            validated_data['secondary_emergency_contact'] = get_or_create(validated_data.pop('secondary_emergency_contact'), EmergencyContact)
        
        return super().update(instance, validated_data)

    class Meta:
        model = Patient
        fields = '__all__'

def get_or_create(data, model):
    # This function is needed because of the nested serializers
    if data.get('id'):
        return get_object_or_404(model, id=data.get('id'))
    elif model == Address:
        return Address.objects.create(**data)
    elif model == EmergencyContact:
        return EmergencyContact.objects.create(
            address = get_or_create(data.pop('address'), Address), 
            **data
        )