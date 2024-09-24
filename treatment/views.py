from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from appointment.models import Appointment, ReferralAppointment
from .models import Treatment
from .serializers import (
    TreatmentCreateSerializer,
    TreatmentListSerializer, 
    TreatmentSerializer, 
    TreatmentUpdateSerializer, 
    TreatmentReferralUpdateSerializer
    )
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication, TokenAuthentication
)
from staff.permissions import (
    IsPatientManager,
    IsSuperUser,
    IsDoctor
)
from patient.permissions import (
    IsPatient
)


class TreatmentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsDoctor | IsPatient]

    def post(self, request, *args, **kwargs):
        # Get appointment ID from request data
        appointment_id = request.data.get('appointment')

        if not appointment_id:
            return Response({"error": "Appointment ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the Appointment by ID
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Determine if the appointment is a referral appointment
        try:
            referral_appointment = ReferralAppointment.objects.get(appointment=appointment)
            is_referral = True
        except ReferralAppointment.DoesNotExist:
            is_referral = False

        if is_referral:
            # Handle referral Treatments
            treatments = Treatment.objects.filter(referral_appointment=referral_appointment)
            if treatments.exists():
                # Return existing Treatments
                serializer = TreatmentSerializer(treatments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # No existing Treatments, create a new one
                serializer = TreatmentCreateSerializer(data=request.data)
                if serializer.is_valid():
                    treatment = serializer.save()
                    # Update appointment status to 'in_progress'
                    appointment.status = 'in_progress'
                    appointment.save()
                    response_serializer = TreatmentSerializer(treatment)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle regular Treatments
            treatments = Treatment.objects.filter(appointment=appointment)
            if treatments.exists():
                # Return existing Treatments
                serializer = TreatmentSerializer(treatments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # No existing Treatments, create a new one
                if appointment.status == 'booked':
                    serializer = TreatmentCreateSerializer(data=request.data)
                    if serializer.is_valid():
                        treatment = serializer.save()
                        # Update appointment status to 'in_progress'
                        appointment.status = 'in_progress'
                        appointment.save()
                        response_serializer = TreatmentSerializer(treatment)
                        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(
                        {"error": "No treatments found and appointment is not 'booked'"},
                        status=status.HTTP_404_NOT_FOUND
                    )


class TreatmentUpdateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_object(self, pk):
        try:
            return Treatment.objects.get(pk=pk)
        except Treatment.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        treatment = self.get_object(pk)
        appointment = treatment.appointment
        appointment_doctor = appointment.doctor

        # Access referral_doctor from treatment.referral_appointment
        if treatment.referral_appointment:
            referral_doctor = treatment.referral_appointment.referral_doctor
        else:
            referral_doctor = None

        # Ensure treatment has not been marked as completed
        if treatment.status == 'completed':
            return Response({"error": "Treatment has been completed and cannot be updated."}, status=status.HTTP_403_FORBIDDEN)

        # Determine who is making the update
        if request.user.id == appointment_doctor.id:
            # Appointment doctor is making the update
            if treatment.is_referral and treatment.referral and treatment.referral.referral_conclusion:
                # Referral doctor has already updated the conclusion, so this is the final update
                serializer = TreatmentUpdateSerializer(treatment, data=request.data, partial=True)
                # Finalize treatment after this update
                treatment.status = 'completed'
                treatment.save()
            else:
                # Regular update by appointment doctor
                serializer = TreatmentUpdateSerializer(treatment, data=request.data, partial=True)
        elif referral_doctor and request.user.id == referral_doctor.id:
            # Referral doctor is making the update
            serializer = TreatmentReferralUpdateSerializer(treatment, data=request.data, partial=True)
        else:
            # Neither the appointment doctor nor the referral doctor
            return Response({"error": "You are not authorized to update this treatment."}, status=status.HTTP_403_FORBIDDEN)

        # Validate and save the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TreatmentDetailView(APIView):

    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = [IsAuthenticated, IsDoctor | IsPatient]

    def get_object(self, pk):
        try:
            return Treatment.objects.get(pk=pk)
        except Treatment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        treatment = self.get_object(pk)
        serializer = TreatmentSerializer(treatment)
        return Response(serializer.data)


class TreatmentListView(APIView):

    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = [IsAuthenticated, IsDoctor | IsPatient]

    def get(self, request, patient_id, format=None):
        category = request.query_params.get('category', None)

        # Фильтруем Treatment по patient_id
        queryset = Treatment.objects.filter(appointment__patient_id=patient_id)

        # Фильтрация по категории, если указана
        if category:
            queryset = queryset.filter(category__icontains=category)

        # Сериализация данных
        serializer = TreatmentListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)