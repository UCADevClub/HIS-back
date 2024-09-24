from rest_framework import serializers
from django.core.exceptions import ValidationError
from appointment.models import Appointment, ReferralAppointment
from appointment.serializers import (AppointmentCreateSerializer, AppointmentSerializer, AppointmentTreatmentListSerializer, AppointmentTreatmentSerializer,
                                     ReferralAppointmentCreateSerializer,ReferralAppointmentSerializer,)
from .models import Medications, ObjectiveExamination, Referral, Treatment


class ObjectiveExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectiveExamination
        fields = '__all__'

    def create(self, validated_data):
        # Создаем новый объект ObjectiveExamination
        return ObjectiveExamination.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Обновляем существующий объект ObjectiveExamination
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


#Referral Serializers
class ReferralSerializer(serializers.ModelSerializer):
    appointment = AppointmentCreateSerializer()

    class Meta:
        model = Referral
        fields = '__all__'


class ReferralCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referral
        fields = '__all__'

    def create(self, validated_data):
        # Extract appointment data
        appointment_data = validated_data.pop('appointment', None)
        
        # Create the Referral instance
        referral = Referral.objects.create(**validated_data)
        
        # If appointment data is provided, update the related Appointment
        if appointment_data:
            # Get or create the related Appointment instance
            appointment_id = appointment_data.get('id')
            if appointment_id:
                appointment = Appointment.objects.filter(id=appointment_id).first()
                if appointment:
                    appointment.is_referral = True
                    appointment.save()
        
        return referral

class ReferralUpdateConclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['referral_conclusion']

    def update(self, instance, validated_data):
        # Update only the referral_conclusion field
        instance.referral_conclusion = validated_data.get('referral_conclusion', instance.referral_conclusion)
        instance.save()
        return instance


class ReferralDoctorUpdateSerializer(serializers.ModelSerializer):
    appointment = AppointmentCreateSerializer()

    class Meta:
        model = Referral
        fields = ['appointment']

    def create(self, validated_data):
        appointment_data = validated_data.pop('appointment', None)

        # Create or update the appointment
        if appointment_data:
            appointment_serializer = AppointmentCreateSerializer(data=appointment_data)
            if appointment_serializer.is_valid(raise_exception=True):
                appointment = appointment_serializer.save()
                # Set `is_referral` to True
                appointment.is_referral = True
                appointment.save()
        else:
            appointment = None
        
        # Create a new Referral instance
        referral = Referral.objects.create(appointment=appointment, **validated_data)
        return referral

    def update(self, instance, validated_data):
        appointment_data = validated_data.pop('appointment', None)

        # Update or create the appointment
        if appointment_data:
            appointment_id = appointment_data.get('id', None)
            
            if appointment_id:
                try:
                    # Update existing appointment
                    appointment = Appointment.objects.get(id=appointment_id)
                    # Set `is_referral` to True
                    appointment.is_referral = True
                    appointment.save()
                except Appointment.DoesNotExist:
                    raise serializers.ValidationError("Appointment does not exist")
            else:
                # Create a new appointment
                appointment_serializer = AppointmentCreateSerializer(data=appointment_data)
                if appointment_serializer.is_valid(raise_exception=True):
                    appointment = appointment_serializer.save()
                    # Set `is_referral` to True
                    appointment.is_referral = True
                    appointment.save()
            
            # Assign the appointment to the referral
            instance.appointment = appointment

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the updated referral instance
        instance.save()
        return instance


class MedicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medications
        fields = '__all__'


#Treatment Serializers
class TreatmentCreateSerializer(serializers.ModelSerializer):
    objective_examination = ObjectiveExaminationSerializer(required=False, allow_null=True)
    referral = ReferralCreateSerializer(required=False, allow_null=True)
    medications = MedicationsSerializer(many=True, required=False, allow_null=True)
    appointment = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.all(), required=True)
    referral_appointment = ReferralAppointmentCreateSerializer(required=False, allow_null=True)

    class Meta:
        model = Treatment
        fields = '__all__'

    def validate(self, data):
        # Check if is_referral is True, referral_doctor must be provided
        if data.get('is_referral'):
            referral_appointment_data = data.get('referral_appointment')
            if not referral_appointment_data or not referral_appointment_data.get('referral_doctor'):
                raise ValidationError({
                    'referral_doctor': 'Referral doctor is required when treatment is a referral.'
                })
        return data

    def create(self, validated_data):
        objective_examination_data = validated_data.pop('objective_examination', None)
        referral_data = validated_data.pop('referral', None)
        medications_data = validated_data.pop('medications', [])
        appointment = validated_data.pop('appointment')
        referral_appointment_data = validated_data.pop('referral_appointment', None)

        appointment.status = "in_progress"
        appointment.save()

        objective_examination = None
        if objective_examination_data:
            objective_examination = ObjectiveExamination.objects.create(**objective_examination_data)

        treatment = Treatment.objects.create(
            objective_examination=objective_examination,
            appointment=appointment,
            **validated_data
        )

        if treatment.is_referral and referral_appointment_data:
            # Create the Referral object
            if referral_data:
                referral = Referral.objects.create(appointment=appointment, **referral_data)
            else:
                referral = Referral.objects.create(appointment=appointment)

            treatment.referral = referral
            treatment.save()

            # **Ensure 'appointment' in referral_appointment_data is a pk**
            referral_appointment_data['appointment'] = appointment.pk

            # Create ReferralAppointment without treatment
            referral_appointment_serializer = ReferralAppointmentCreateSerializer(data=referral_appointment_data)
            referral_appointment_serializer.is_valid(raise_exception=True)
            referral_appointment = referral_appointment_serializer.save()

            # Assign the treatment to the ReferralAppointment
            referral_appointment.treatment = treatment
            referral_appointment.save()

            # Link the ReferralAppointment to the Treatment
            treatment.referral_appointment = referral_appointment
            treatment.save()

        if medications_data:
            for medication_data in medications_data:
                medication, created = Medications.objects.get_or_create(**medication_data)
                treatment.medications.add(medication)

        return treatment


class TreatmentSerializer(serializers.ModelSerializer):
    objective_examination = ObjectiveExaminationSerializer(required=False, allow_null=True)
    referral = ReferralSerializer(required=False, allow_null=True)
    medications = MedicationsSerializer(many=True, required=False, allow_null=True)
    appointment = AppointmentTreatmentSerializer()
    referral_appointment = ReferralAppointmentSerializer(required=False, allow_null=True)  # Add this line

    class Meta:
        model = Treatment
        fields = '__all__'


class TreatmentUpdateSerializer(serializers.ModelSerializer):
    objective_examination = ObjectiveExaminationSerializer(required=False, allow_null=True)
    referral = ReferralDoctorUpdateSerializer(required=False, allow_null=True)
    medications = MedicationsSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Treatment
        fields = [
            'objective_examination',
            'examination_plan',
            'lab_tests',
            'referral',
            'justification_and_formulation',
            'recommendations',
            'medications',
            'category',
            'status'
        ]

    def update(self, instance, validated_data):
        # Handle ObjectiveExamination updates
        objective_examination_data = validated_data.pop('objective_examination', None)
        referral_data = validated_data.pop('referral', None)
        medications_data = validated_data.pop('medications', [])

        # Update or create ObjectiveExamination
        if objective_examination_data:
            if instance.objective_examination:
                objective_examination_serializer = ObjectiveExaminationSerializer(
                    instance.objective_examination, data=objective_examination_data, partial=True
                )
                if objective_examination_serializer.is_valid(raise_exception=True):
                    objective_examination_serializer.save()
            else:
                objective_examination_serializer = ObjectiveExaminationSerializer(data=objective_examination_data)
                if objective_examination_serializer.is_valid(raise_exception=True):
                    instance.objective_examination = objective_examination_serializer.save()

        # Update or create Referral
        if referral_data and instance.appointment.is_referral:
            if instance.referral:
                referral_serializer = ReferralDoctorUpdateSerializer(
                    instance.referral, data=referral_data, partial=True
                )
                if referral_serializer.is_valid(raise_exception=True):
                    referral_serializer.save()
            else:
                raise serializers.ValidationError("Referral does not exist for this treatment.")

        # Update medications
        if medications_data:
            new_medications = []
            for medication_data in medications_data:
                medication, created = Medications.objects.get_or_create(**medication_data)
                new_medications.append(medication)
            instance.medications.set(new_medications)

        # Update the remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TreatmentReferralUpdateSerializer(serializers.ModelSerializer):
    referral = ReferralUpdateConclusionSerializer()
    lab_tests = serializers.FileField(required=False)  # For single file uploads

    class Meta:
        model = Treatment
        fields = ['referral', 'lab_tests']

    def update(self, instance, validated_data):
        # Get the referral data and lab_tests data
        referral_data = validated_data.get('referral', None)
        lab_tests_data = validated_data.get('lab_tests', None)

        # Update the referral conclusion
        if referral_data:
            referral = instance.referral  # Ensure that referral exists
            if referral:
                referral_serializer = ReferralUpdateConclusionSerializer(
                    referral, data=referral_data, partial=True
                )
                if referral_serializer.is_valid(raise_exception=True):
                    referral_serializer.save()
            else:
                raise serializers.ValidationError("No referral exists for this treatment.")

        # Handle lab tests updates
        if lab_tests_data is not None:
            instance.lab_tests = lab_tests_data

        instance.save()
        return instance

class TreatmentListSerializer(serializers.ModelSerializer):
    appointment = AppointmentTreatmentListSerializer()

    class Meta:
        model = Treatment
        fields = [
            'id',
            "appointment",  
            "category",
            "justification_and_formulation"
        ]