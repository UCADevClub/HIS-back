from rest_framework import serializers
from patient.serializers import PatientSerializer
from staff.serializers import DoctorSerializer
from .models import Appointment

class AppointmentCreateSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'talon', 'complaint', 'status', 'payment_status']

    def create(self, validated_data):
        appointment = Appointment.objects.create(**validated_data)
        return appointment


class AppointmentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    
    
class AppointmentPaymentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['payment_status']

    def update(self, instance, validated_data):
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)
        instance.save()
        return instance