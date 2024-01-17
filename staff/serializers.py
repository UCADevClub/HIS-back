from rest_framework import serializers
from user_authentication.serializers import BaseUserSerializer
from staff.models import Doctor
from user_authentication.models import BaseUser


class DoctorSerializer(serializers.ModelSerializer):
    doctor = BaseUserSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'
