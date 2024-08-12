from rest_framework import serializers

from appointment.models import Appointment
from appointment.serializers import AppointmentCreateSerializer
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
    class Meta:
        model = Referral
        fields = '__all__'

    def create(self, validated_data):
        # Создаем новый объект Referral
        return Referral.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Обновляем существующий объект Referral
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class MedicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medications
        fields = '__all__'


class TreatmentCreateSerializer(serializers.ModelSerializer):
    objective_examination = ObjectiveExaminationSerializer(required=False, allow_null=True)
    referral = ReferralSerializer(required=False, allow_null=True)
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
    appointment = AppointmentCreateSerializer()  # Use AppointmentSerializer to show full details

    class Meta:
        model = Treatment
        fields = '__all__'


class TreatmentUpdateSerializer(serializers.ModelSerializer):
    objective_examination = ObjectiveExaminationSerializer(required=False, allow_null=True)
    referral = ReferralSerializer(required=False, allow_null=True)
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
                referral_serializer = ReferralSerializer(
                    instance.referral, data=referral_data, partial=True
                )
                if referral_serializer.is_valid(raise_exception=True):
                    instance.referral = referral_serializer.save()
            else:
                referral_serializer = ReferralSerializer(data=referral_data)
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