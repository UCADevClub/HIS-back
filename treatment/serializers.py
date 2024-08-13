from rest_framework import serializers

from appointment.models import Appointment
from appointment.serializers import AppointmentCreateSerializer, AppointmentSerializer
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


class ReferralSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer()

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


class TreatmentCreateSerializer(serializers.ModelSerializer):
    objective_examination = ObjectiveExaminationSerializer(required=False, allow_null=True)
    referral = ReferralCreateSerializer(required=False, allow_null=True)
    medications = MedicationsSerializer(many=True, required=False, allow_null=True)
    appointment = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.all(), required=False)

    class Meta:
        model = Treatment
        fields = '__all__'

    def create(self, validated_data):
        objective_examination_data = validated_data.pop('objective_examination', None)
        referral_data = validated_data.pop('referral', None)
        medications_data = validated_data.pop('medications', [])
        appointment = validated_data.pop('appointment', None)

        # Create or update ObjectiveExamination
        objective_examination = None
        if objective_examination_data:
            objective_examination = ObjectiveExamination.objects.create(**objective_examination_data)

        # Create or update Referral
        referral = None
        if referral_data:
            referral = Referral.objects.create(**referral_data)

        # Create Treatment
        treatment = Treatment.objects.create(
            objective_examination=objective_examination,
            referral=referral,
            appointment=appointment,
            **validated_data
        )

        # Add Medications
        if medications_data:
            for medication_data in medications_data:
                medication, created = Medications.objects.get_or_create(**medication_data)
                treatment.medications.add(medication)

        return treatment

class TreatmentSerializer(serializers.ModelSerializer):
    objective_examination = ObjectiveExaminationSerializer(required=False, allow_null=True)
    referral = ReferralSerializer(required=False, allow_null=True)
    medications = MedicationsSerializer(many=True, required=False, allow_null=True)
    appointment = AppointmentSerializer()

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
            'medications'
        ]

    def update(self, instance, validated_data):
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
        if referral_data:
            if instance.referral:
                referral_serializer = ReferralDoctorUpdateSerializer(
                    instance.referral, data=referral_data, partial=True
                )
                if referral_serializer.is_valid(raise_exception=True):
                    instance.referral = referral_serializer.save()
            else:
                referral_serializer = ReferralDoctorUpdateSerializer(data=referral_data)
                if referral_serializer.is_valid(raise_exception=True):
                    instance.referral = referral_serializer.save()

        # Update medications
        if medications_data:
            new_medications = []
            for medication_data in medications_data:
                medication, created = Medications.objects.get_or_create(**medication_data)
                new_medications.append(medication)
            instance.medications.set(new_medications)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
