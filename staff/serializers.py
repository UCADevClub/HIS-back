from rest_framework import serializers
from user_authentication.serializers import BaseUserSerializer
from staff.models import Doctor
from user_authentication.models import BaseUser


class DoctorSerializer(serializers.ModelSerializer):
    doctor = BaseUserSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        doctor_data = validated_data.pop('doctor')
        doctor_user = BaseUser.objects.create(**doctor_data)
        doctor_object = Doctor()
        doctor = doctor_object.doctor.objects.create(doctor=doctor_user, **validated_data)
        return doctor
