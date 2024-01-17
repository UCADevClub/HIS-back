from rest_framework import serializers
from .models import EmergencyContact, Patient
from user_authentication.serializers import BaseUserSerializer, AddressSerializer
from user_authentication.models import Address
from django.shortcuts import get_object_or_404

class EmergencyContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    address = AddressSerializer()

    def create(self, validated_data):
        if validated_data.get('address'):
            validated_data['address'] = get_or_create(validated_data.pop('address'), AddressSerializer)
        return super(EmergencyContactSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('address'):
            validated_data['address'] = get_or_create(validated_data.pop('address'), AddressSerializer)
        return super().update(instance, validated_data)

    class Meta:
        model = EmergencyContact
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'address',
        ]


class PatientSerializer(BaseUserSerializer):
    primary_address = AddressSerializer()
    primary_emergency_contact = EmergencyContactSerializer()
    secondary_emergency_contact = EmergencyContactSerializer()

    def create(self, validated_data):
        if validated_data.get('primary_address'):
            validated_data['primary_address'] = get_or_create(validated_data.pop('primary_address'), AddressSerializer)
        if validated_data.get('primary_emergency_contact'):
            validated_data['primary_emergency_contact'] = get_or_create(validated_data.pop('primary_emergency_contact'),
                                                                    EmergencyContactSerializer)
        if validated_data.get('secondary_emergency_contact'):
            validated_data['secondary_emergency_contact'] = get_or_create(validated_data.pop('secondary_emergency_contact'),
                                                                      EmergencyContactSerializer)
        user = super(PatientSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if validated_data.get('primary_address'):
            validated_data['primary_address'] = get_or_create(validated_data.pop('primary_address'), AddressSerializer)
        if validated_data.get('primary_emergency_contact'):
            validated_data['primary_emergency_contact'] = get_or_create(validated_data.pop('primary_emergency_contact'),
                                                                        EmergencyContactSerializer)
        if validated_data.get('secondary_emergency_contact'):
            validated_data['secondary_emergency_contact'] = get_or_create(
                validated_data.pop('secondary_emergency_contact'), EmergencyContactSerializer)

        return super().update(instance, validated_data)

    class Meta:
        model = Patient
        fields = [
            'inn', 
            'first_name', 
            'last_name', 
            'email', 
            'gender',
            'password',
            'phone_number', 
            'date_of_birth', 
            'primary_address', 
            'primary_emergency_contact', 
            'secondary_emergency_contact', 
        ]
        extra_kwargs = {
            'password': {
                'write_only': True, 
                'required': False},
        }


def get_or_create(data, serializer):
    # This function is needed because of the nested serializers
    if isinstance(data, (int, str)):
        return get_object_or_404(serializer.Meta.model, id=data)
    elif data.get('id'):
        return get_object_or_404(serializer.Meta.model, id=data.get('id'))
    s = serializer(data=data)
    if s.is_valid():
        return s.save()
    else:
        print(s.errors)
        return s.errors