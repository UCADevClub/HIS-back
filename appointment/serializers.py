from rest_framework import serializers
from patient.models import Patient
from patient.serializers import PatientAppointmentSerializer, PatientGetSerializer, PatientSerializer, PatientTreatmentSerializer
from staff.models import Doctor
from staff.serializers import DoctorAppointmentSerializer,DoctorReferralAppointmentSerializer
from .models import Appointment,ReferralAppointment
from treatment.models import Treatment
class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientAppointmentSerializer()
    doctor = DoctorAppointmentSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'talon', 'reason', 'status', 'payment_status', 'doctor','patient', 'created_at']


class AppointmentTreatmentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ['doctor','reason', 'status','created_at']


class AppointmentTreatmentSerializer(serializers.ModelSerializer):
    patient = PatientTreatmentSerializer()
    doctor = DoctorAppointmentSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'talon', 'reason', 'status', 'payment_status', 'doctor', 'patient', 'created_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta:
        model = Appointment
        fields = ['id', 'talon', 'reason', 'status', 'payment_status', 'doctor', 'patient']

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

class ReferralAppointmentCreateSerializer(serializers.ModelSerializer):
    appointment = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.all())
    referral_doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())  # Add referral_doctor field
    treatment = serializers.PrimaryKeyRelatedField(read_only=True) # Add treatment field

    class Meta:
        model = ReferralAppointment
        fields = ['appointment', 'referral_doctor', 'treatment', 'created_at']

    def create(self, validated_data):
        appointment = validated_data['appointment']
        referral_doctor = validated_data['referral_doctor']

        referral_appointment = ReferralAppointment.objects.create(
            appointment=appointment,
            referral_doctor=referral_doctor
        )
        return referral_appointment

class ReferralAppointmentSerializer(serializers.ModelSerializer):
    appointment = AppointmentTreatmentSerializer()
    referral_doctor = DoctorReferralAppointmentSerializer()
    class Meta:
        model = ReferralAppointment
        fields = ['id','appointment', 'referral_doctor','created_at']