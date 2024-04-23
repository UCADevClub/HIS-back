from rest_framework.serializers import ModelSerializer

from user_authentication.serializers import (
    BaseUserCreateSerializer,
    BaseUserSerializer,
)
from patient.models import Patient
from user_authentication.models import Address, EmergencyContact


class EmergencyContactCreateSerializer(ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'phone_number',
        )

    def create(self, validated_data):
        emergency_contact_instance = EmergencyContact.objects.create(
            **validated_data,
        )
        return emergency_contact_instance


class EmergencyContactSerializer(ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ("first_name",
                  'middle_name',
                  'last_name',
                  "phone_number",
                  )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            "first_name", instance.first_name)
        instance.middle_name = validated_data.get(
            "middle_name", instance.middle_name)
        instance.last_name = validated_data.get(
            "last_name", instance.last_name)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number)

        instance.save()
        return instance


class PatientCreateSerializer(BaseUserCreateSerializer):
    primary_emergency_contact = EmergencyContactCreateSerializer()
    secondary_emergency_contact = EmergencyContactCreateSerializer(required=False)

    class Meta:
        model = Patient
        fields = BaseUserCreateSerializer.Meta.fields + (
            'primary_emergency_contact',
            'secondary_emergency_contact',
            'marital_status',
        )

    def create(self, validated_data):
        primary_emergency_contact_data = validated_data.pop('primary_emergency_contact')
        secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact', None)

        primary_emergency_contact_instance = EmergencyContactCreateSerializer.create(
            EmergencyContactCreateSerializer(),
            validated_data=primary_emergency_contact_data
        )

        marital_status = validated_data.pop('marital_status')
        address_data = validated_data.pop('address')
        address_instance = Address.objects.create(**address_data)
        patient_instance = Patient.objects.create_user(
            **validated_data,
            address=address_instance,
            marital_status=marital_status,
            primary_emergency_contact=primary_emergency_contact_instance,
        )
        if secondary_emergency_contact_data:
            secondary_emergency_contact_instance = EmergencyContactCreateSerializer.create(
                EmergencyContactCreateSerializer(), validated_data=secondary_emergency_contact_data
            )
            patient_instance.secondary_emergency_contact = secondary_emergency_contact_instance

        return patient_instance


class PatientSerializer(BaseUserSerializer):
    primary_emergency_contact = EmergencyContactSerializer()
    secondary_emergency_contact = EmergencyContactSerializer()

    class Meta(BaseUserSerializer.Meta):
        model = Patient
        fields = BaseUserSerializer.Meta.fields + (
            'marital_status',
            'primary_emergency_contact',
            'secondary_emergency_contact'
        )

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        primary_emergency_contact_data = validated_data.pop(
            'primary_emergency_contact', None)
        primary_emergency_contact_instance = instance.primary_emergency_contact
        if primary_emergency_contact_data:
            primary_emergency_contact_serializer = EmergencyContactSerializer(primary_emergency_contact_instance,
                                                                              data=primary_emergency_contact_data)
            if primary_emergency_contact_serializer.is_valid():
                primary_emergency_contact_serializer.save()

        secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact', None)
        if secondary_emergency_contact_data is not None:  # Check if secondary_emergency_contact_data is provided
            # If secondary_emergency_contact_data is provided, create or update the secondary emergency contact
            if instance.secondary_emergency_contact:  # If the secondary emergency contact already exists, update it
                secondary_emergency_contact_instance = instance.secondary_emergency_contact
                secondary_emergency_contact_serializer = EmergencyContactSerializer(
                    secondary_emergency_contact_instance, data=secondary_emergency_contact_data)
            else:  # If the secondary emergency contact doesn't exist, create it
                secondary_emergency_contact_serializer = EmergencyContactSerializer(
                    data=secondary_emergency_contact_data)
            if secondary_emergency_contact_serializer.is_valid():
                secondary_emergency_contact_serializer.save()
                instance.secondary_emergency_contact = secondary_emergency_contact_serializer.instance  # Assign the
                # newly created or updated instance to the secondary_emergency_contact field

        instance.save()

        return instance
