from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from appointment.models import Appointment
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

    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = [IsAuthenticated, IsDoctor | IsPatient]

    def post(self, request, *args, **kwargs):
        # Получаем ID из запроса
        appointment_id = request.data.get('appointment')
        
        if not appointment_id:
            return Response({"error": "Appointment ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Поиск Appointment по ID
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if not appointment.is_referral:
            # Если is_referral = False
            if appointment.status == 'booked':
                # Создание нового Treatment
                serializer = TreatmentCreateSerializer(data=request.data)
                if serializer.is_valid():
                    treatment = serializer.save()
                    # Обновляем статус appointment на 'in_progress'
                    appointment.status = "in_progress"
                    appointment.save()
                    response_serializer = TreatmentSerializer(treatment)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif appointment.status == 'in_progress':
                # Возвращаем существующие Treatment
                treatments = Treatment.objects.filter(appointment=appointment)
                if not treatments.exists():
                    return Response({"error": "No treatments found"}, status=status.HTTP_404_NOT_FOUND)
                serializer = TreatmentSerializer(treatments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            # Если is_referral = True
            treatments = Treatment.objects.filter(referral__appointment=appointment)
            if not treatments.exists():
                return Response({"error": "No treatments found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Обновляем статус referral на 'in_progress'
            for treatment in treatments:
                if treatment.referral and treatment.referral.appointment.status == 'booked':
                    treatment.referral.appointment.status = 'in_progress'
                    treatment.referral.appointment.save()  # Сохраняем изменения в referral.appointment
                    treatment.save()  # Сохраняем изменения в treatment
            
            serializer = TreatmentSerializer(treatments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid appointment status or referral status"}, status=status.HTTP_400_BAD_REQUEST)


class TreatmentUpdateView(APIView):
    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = [IsAuthenticated, IsDoctor]


    def get_object(self, pk):
        try:
            return Treatment.objects.get(pk=pk)
        except Treatment.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        treatment = self.get_object(pk)
        appointment = treatment.appointment
        referral = treatment.referral

        # Determine the appropriate serializer based on the presence of referral
        if referral is None:
            serializer = TreatmentUpdateSerializer(treatment, data=request.data, partial=True)
            
            # Check if the user is the doctor associated with the Appointment
            if request.user.id != appointment.doctor.id:
                return Response({"error": "You are not authorized to update this treatment."}, status=status.HTTP_403_FORBIDDEN)
        
        else:
            if request.user.id == appointment.doctor.id:
                serializer = TreatmentUpdateSerializer(treatment, data=request.data, partial=True)
            elif request.user.id == referral.appointment.doctor.id:
                serializer = TreatmentReferralUpdateSerializer(treatment, data=request.data, partial=True)
            
            # Check if the user is either the doctor associated with the Appointment or the doctor associated with the Referral
            if request.user.id not in [appointment.doctor.id, referral.appointment.doctor.id]:
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