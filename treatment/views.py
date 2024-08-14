from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from appointment.models import Appointment
from .models import Treatment
from .serializers import (
    TreatmentCreateSerializer, 
    TreatmentSerializer, 
    TreatmentUpdateSerializer, 
    TreatmentReferralUpdateSerializer
    )

class TreatmentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TreatmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            treatment = serializer.save()
            response_serializer = TreatmentCreateSerializer(treatment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TreatmentDetailView(APIView):
    
    def get_object(self, pk):
        try:
            return Treatment.objects.get(pk=pk)
        except Treatment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        treatment = self.get_object(pk)
        serializer = TreatmentSerializer(treatment)
        return Response(serializer.data)
    

class TreatmentByAppointmentView(APIView):
    def post(self, request, format=None):
        appointment_id = request.data.get('appointment_id')
        
        if not appointment_id:
            return Response({"error": "Appointment ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Поиск Appointment по ID
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Определение фильтра
        if appointment.is_referral:
            # Если is_referral=True, ищем Treatment по referral.appointment
            treatments = Treatment.objects.filter(referral__appointment=appointment)
        else:
            # Если is_referral=False, ищем Treatment по appointment
            treatments = Treatment.objects.filter(appointment=appointment)

        # Если нет результатов
        if not treatments.exists():
            return Response({"error": "No treatments found"}, status=status.HTTP_404_NOT_FOUND)

        # Сериализация и возврат данных
        serializer = TreatmentSerializer(treatments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TreatmentUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Treatment.objects.get(pk=pk)
        except Treatment.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        treatment = self.get_object(pk)
        serializer = TreatmentUpdateSerializer(treatment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TreatmentReferralUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Treatment.objects.get(pk=pk)
        except Treatment.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        treatment = self.get_object(pk)
        serializer = TreatmentReferralUpdateSerializer(treatment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)