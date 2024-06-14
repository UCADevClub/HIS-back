from patient.models import Patient
from user_authentication.serializers import (
    StandardUserSerializer,
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
        secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact')

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
