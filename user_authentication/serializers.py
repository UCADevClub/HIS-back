from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from user_authentication.models import (
    Address,
    EmergencyContact,
    BaseUser,
    StandardUser,
)


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class EmergencyContactSerializer(ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'


class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'


class StandardUserSerializer(ModelSerializer):
    address = AddressSerializer()
    primary_emergency_contact = EmergencyContactSerializer()
    secondary_emergency_contact = EmergencyContactSerializer(required=False)
    date_of_birth =serializers.DateField(required = False, allow_null = True,
        input_formats=['%d-%m-%Y']
    )

    class Meta:
        model = StandardUser
        fields = (
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

        return StandardUser.objects.create(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

    # def update(self, instance, validated_data):
    #
    #     primary_emergency_contact_data = validated_data.pop(
    #         'primary_emergency_contact', None)
    #     validated_data['primary_emergency_contact'] =
    #     primary_emergency_contact_instance = instance.primary_emergency_contact
    #     if primary_emergency_contact_data:
    #         primary_emergency_contact_serializer = EmergencyContactSerializer(
    #             primary_emergency_contact_instance,
    #             data=primary_emergency_contact_data)
    #         if primary_emergency_contact_serializer.is_valid():
    #             primary_emergency_contact_serializer.save()
    #
    #     secondary_emergency_contact_data = validated_data.pop('secondary_emergency_contact', None)
    #     if secondary_emergency_contact_data is not None:  # Check if secondary_emergency_contact_data is provided
    #         # If secondary_emergency_contact_data is provided, create or update the secondary emergency contact
    #         if instance.secondary_emergency_contact:  # If the secondary emergency contact already exists, update it
    #             secondary_emergency_contact_instance = instance.secondary_emergency_contact
    #             secondary_emergency_contact_serializer = EmergencyContactSerializer(
    #                 secondary_emergency_contact_instance, data=secondary_emergency_contact_data)
    #         else:  # If the secondary emergency contact doesn't exist, create it
    #             secondary_emergency_contact_serializer = EmergencyContactSerializer(
    #                 data=secondary_emergency_contact_data)
    #         if secondary_emergency_contact_serializer.is_valid():
    #             secondary_emergency_contact_serializer.save()
    #             instance.secondary_emergency_contact = secondary_emergency_contact_serializer.instance  # Assign the
    #             # newly created or updated instance to the secondary_emergency_contact field
    #
    #     instance.save()
    #
    #     return instance
