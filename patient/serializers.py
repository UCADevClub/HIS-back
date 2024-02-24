from rest_framework.serializers import ModelSerializer, Serializer
from user_authentication.serializers import (
    BaseUserCreateSerializer,
    BaseUserSerializer,
    AddressSerializer,
    AddressCreateSerializer
)
from patient.models import Patient, EmergencyContact
from user_authentication.models import Address


class EmergencyContactCreateSerializer(Serializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'

    # address = AddressSerializer()


class EmergencyContactSerializer(Serializer):
    class Meta:
        model = EmergencyContact
        fields = ['first_name',
                  'middle_name',
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

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        print(f'{validated_data=}')
        print(f'{address_data=}')
        emergency_contact_instance = EmergencyContact(validated_data=validated_data)
        emergency_contact_instance.address = Address(validated_data=address_data)
        return emergency_contact_instance


class PatientCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model = Patient
        fields = BaseUserCreateSerializer.Meta.fields + (
                'primary_emergency_contact',
                'secondary_emergency_contact',
                'marital_status',
        )

    primary_emergency_contact = EmergencyContactCreateSerializer()
    secondary_emergency_contact = EmergencyContactCreateSerializer()

    def create(self, validated_data):
        primary_emergency_contact_data = validated_data.pop('primary_emergency_contact')
        secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact')
        marital_status_data = validated_data.pop('marital_status')
        print(f'{validated_data=}')
        base_user = super().create(validated_data=validated_data)
        return base_user


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
            primary_emergency_contact_serializer = EmergencyContactSerializer(primary_emergency_contact_instance, data=primary_emergency_contact_data)
            if primary_emergency_contact_serializer.is_valid():
                primary_emergency_contact_serializer.save()

        if secondary_emergency_contact_data:
            secondary_emergency_contact_serializer = EmergencyContactSerializer(secondary_emergency_contact_instance, data=secondary_emergency_contact_data)
            if secondary_emergency_contact_serializer.is_valid():
                secondary_emergency_contact_serializer.save()

        instance.save()

        return instance
