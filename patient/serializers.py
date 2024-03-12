from django.utils.crypto import get_random_string
from rest_framework.serializers import ModelSerializer

from user_authentication.serializers import (
    BaseUserCreateSerializer,
    BaseUserSerializer,
)
from patient.models import Patient, EmergencyContact
from user_authentication.models import Address


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

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)

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
        password = get_random_string(length=8)
        patient_instance = Patient.objects.create_user(
            **validated_data,
            address=address_instance,
            password=password,
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
    class Meta(BaseUserSerializer.Meta):
        model = Patient
        fields = BaseUserSerializer.Meta.fields + (
            'marital_status',
            'primary_emergency_contact',
            'secondary_emergency_contact'
        )

    primary_emergency_contact = EmergencyContactSerializer()
    secondary_emergency_contact = EmergencyContactSerializer()

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        primary_emergency_contact_data = validated_data.pop('primary_emergency_contact', None)
        primary_emergency_contact_instance = instance.primary_emergency_contact

        secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact', None)
        secondary_emergency_contact_instance = instance.secondary_emergency_contact

        if primary_emergency_contact_data:
            primary_emergency_contact_serializer = EmergencyContactSerializer(primary_emergency_contact_instance,
                                                                              data=primary_emergency_contact_data)
            if primary_emergency_contact_serializer.is_valid():
                primary_emergency_contact_serializer.save()

        if secondary_emergency_contact_data:
            secondary_emergency_contact_serializer = EmergencyContactSerializer(secondary_emergency_contact_instance,
                                                                                data=secondary_emergency_contact_data)
            if secondary_emergency_contact_serializer.is_valid():
                secondary_emergency_contact_serializer.save()

        instance.save()

        return instance
