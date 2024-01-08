from rest_framework import serializers
from .models import EmergencyContact, Patient
from user_authentication.serializers import BaseUserSerializer, AddressSerializer


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'


class PatientSerializer(BaseUserSerializer):
    primary_address = AddressSerializer()
    primary_emergency_contact = EmergencyContactSerializer()
    secondary_emergency_contact = EmergencyContactSerializer()

    class Meta:
        model = Patient
        fields = '__all__'