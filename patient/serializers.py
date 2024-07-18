from patient.models import Patient
from user_authentication.serializers import (
    StandardUserSerializer,
    AddressSerializer,
    EmergencyContactSerializer
)
from user_authentication.models import (
    Address,
    EmergencyContact,
)


class PatientSerializer(StandardUserSerializer):

    class Meta:
        model = Patient
        fields = (
                'id',
                'user_id',
                'first_name',
                'last_name',
                'middle_name',
                'email',
                'citizenship',
                'date_of_birth',
                'phone_number',
                'gender',
                'address',
                'primary_emergency_contact',
                'secondary_emergency_contact',
                'marital_status'
        )

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        primary_emergency_contact_data = validated_data.pop('primary_emergency_contact')
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

        return Patient.objects.create_patient(**validated_data)

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        primary_emergency_contact_data = validated_data.pop('primary_emergency_contact', None)
        secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact', None)

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
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance