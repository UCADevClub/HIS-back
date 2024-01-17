from rest_framework import serializers
from user_authentication.serializers import BaseUserSerializer
from staff.models import Doctor
from patient.serializers import get_or_create, AddressSerializer


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'inn',
            'first_name',
            'last_name',
            'email',
            'gender',
            'date_of_birth',
            'position',
            'specialization',
            'address'
        ]

    def create(self, validated_data):
        if validated_data.get('address'):
            validated_data['address'] = get_or_create(validated_data.pop('address'), AddressSerializer)
        user = super(DoctorSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
