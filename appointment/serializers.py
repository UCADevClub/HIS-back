from rest_framework import serializers
from patient.models import Patient
from patient.serializers import PatientAppointmentSerializer, PatientGetSerializer, PatientSerializer, PatientTreatmentSerializer
from staff.models import Doctor
from staff.serializers import DoctorAppointmentSerializer
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientAppointmentSerializer()
    doctor = DoctorAppointmentSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'talon', 'reason', 'status', 'payment_status', 'is_referral', 'doctor','referral_doctor','patient', 'created_at']


class AppointmentTreatmentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ['doctor','reason', 'status','created_at']


class AppointmentTreatmentSerializer(serializers.ModelSerializer):
    patient = PatientTreatmentSerializer()
    doctor = DoctorAppointmentSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'talon', 'reason', 'status', 'payment_status', 'is_referral', 'doctor', 'patient','referral_doctor', 'created_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    referral_doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Appointment
        fields = ['id', 'talon', 'reason', 'status', 'payment_status', 'is_referral', 'doctor', 'patient','referral_doctor']

    def validate(self, data):
        # If is_referral is True, ensure referral_doctor is provided
        if data.get('is_referral') and not data.get('referral_doctor'):
            raise serializers.ValidationError("A referral doctor must be provided if the appointment is a referral.")

        # If is_referral is False, ensure referral_doctor is set to None
        if not data.get('is_referral'):
            data['referral_doctor'] = None

        return data

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