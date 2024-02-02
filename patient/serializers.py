from rest_framework.serializers import ModelSerializer

from user_authentication.serializers import BaseUserSerializer
from patient.models import Patient, EmergencyContact
from user_authentication.serializers import AddressSerializer


class EmergencyContactSerializer(ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ['first_name',
                  'last_name',
                  "phone_number",
                  "address",
                  ]

    address = AddressSerializer()

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)

        address_data = validated_data.pop('address', None)
        address_instance = instance.address

        if address_data:
            address_serializer = AddressSerializer(address_instance, data=address_data)
            if address_serializer.is_valid():
                address_serializer.save()
        instance.save()
        return instance


class PatientSerializer(BaseUserSerializer):

    class Meta:
        model = Patient
        fields = ['inn',
                  'first_name',
                  'last_name',
                  'email',
                  'date_of_birth',
                  'gender',
                  "phone_number",
                  "primary_address",
                  "primary_emergency_contact",
                  "secondary_emergency_contact",
                  ]

    primary_address = AddressSerializer()
    primary_emergency_contact = EmergencyContactSerializer()
    secondary_emergency_contact = EmergencyContactSerializer()

    def update(self, instance, validated_data):

        instance.email = validated_data.get('email', instance.email)

        primary_address_data = validated_data.pop('primary_address', None)
        primary_address_instance = instance.primary_address

        primary_emergency_contact_data = validated_data.pop('primary_emergency_contact', None)
        primary_emergency_contact_instance = instance.primary_emergency_contact

        secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact', None)
        secondary_emergency_contact_instance = instance.secondary_emergency_contact

        if primary_address_data:
            primary_address_serializer = AddressSerializer(primary_address_instance, data=primary_address_data)
            if primary_address_serializer.is_valid():
                primary_address_serializer.save()

        if primary_emergency_contact_data:
            primary_emergency_contact_serializer = EmergencyContactSerializer(primary_emergency_contact_instance, data=primary_emergency_contact_data)
            if primary_emergency_contact_serializer.is_valid():
                primary_emergency_contact_serializer.save()

        if secondary_emergency_contact_data:
            secondary_emergency_contact_serializer = EmergencyContactSerializer(secondary_emergency_contact_instance, data=secondary_emergency_contact_data)
            if secondary_emergency_contact_serializer.is_valid():
                secondary_emergency_contact_serializer.save()

        instance.save()

        return instance

