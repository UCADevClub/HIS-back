<<<<<<< HEAD
from user_authentication.serializers import BaseUserSerializer, AddressSerializer
from staff.models import Staff
=======
from rest_framework import serializers
from staff.models import Doctor
from patient.serializers import AddressSerializer
>>>>>>> cf1a8777eb6e838685a1ef4bda499c4024008297


class StaffSerializer(BaseUserSerializer):
    class Meta:
        model = Staff
        fields = [
            'inn',
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'gender',
            "phone_number",
            "primary_address",
            'position',
            'specialization',
        ]

    # def create(self, validated_data):
    #     if validated_data.get('address'):
    #         validated_data['address'] = get_or_create(
    #             validated_data.pop('address'), AddressSerializer)
    #     user = super(StaffSerializer, self).create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
    primary_address = AddressSerializer()

    def update(self, instance, validated_data):

        super().update(instance, validated_data)

        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)

        primary_address_data = validated_data.pop('primary_address', None)
        primary_address_instance = instance.primary_address

        if primary_address_data:
            primary_address_serializer = AddressSerializer(
                primary_address_instance, data=primary_address_data)
            if primary_address_serializer.is_valid():
                primary_address_serializer.save()

        instance.save()

        return instance
