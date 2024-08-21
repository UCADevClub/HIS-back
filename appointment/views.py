from datetime import datetime
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentCreateSerializer, AppointmentPaymentStatusUpdateSerializer, AppointmentSerializer, AppointmentStatusUpdateSerializer
from rest_framework.authentication import (
     TokenAuthentication
)
from staff.permissions import (
    IsPatientManager,
    IsSuperUser,
    IsDoctor,
    IsBranchAdministrator
)
from patient.permissions import (
    IsPatient
)

class AppointmentCreateView(APIView):

    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = [IsAuthenticated, IsDoctor | IsPatientManager]


    def post(self, request, *args, **kwargs):
        serializer = AppointmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()
            return Response(
                {
                    "message": "Appointment created successfully",
                    "data": AppointmentCreateSerializer(appointment).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Invalid data",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

   
class AppointmentDetailView(APIView):

    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = [IsAuthenticated, IsDoctor | IsPatient | IsPatientManager]

    def get(self, request, *args, **kwargs):
        appointment_id = kwargs.get('pk')
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {
                    "message": "Appointment not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Prepare response data
        response_data = {}

        # If the appointment status is not 'completed' or 'canceled', find the current_talon
        if appointment.status not in ['completed', 'canceled']:
            speciality_initial = ''.join([s.position[0].upper() for s in appointment.doctor.speciality.all()[:1]])

            # If the talon is '01', use it as the current_talon
            if appointment.talon.endswith('01'):
                response_data["current_talon"] = appointment.talon
            else:
                # Try to find a talon with status 'in_progress'
                current_talon = Appointment.objects.filter(
                    doctor=appointment.doctor,
                    talon__startswith=speciality_initial,
                    status='in_progress'
                ).exclude(id=appointment.id).first()

                # If no 'in_progress' talon, set current_talon to an empty string
                if not current_talon:
                    response_data["current_talon"] = ""
                else:
                    response_data["current_talon"] = current_talon.talon

                # Find the last completed talon
                last_completed_talon = Appointment.objects.filter(
                    doctor=appointment.doctor,
                    talon__startswith=speciality_initial,
                    status='completed'
                ).order_by('-created_at').first()

                response_data["last_completed_talon"] = last_completed_talon.talon if last_completed_talon else None

        serializer = AppointmentSerializer(appointment)
        response_data.update(serializer.data)

        return Response(
            {
                "message": "Appointment details fetched successfully",
                "data": response_data
            },
            status=status.HTTP_200_OK
        )


class AppointmentStatusUpdateView(APIView):

    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = [IsAuthenticated | IsPatientManager | IsDoctor | IsPatient,]

    def patch(self, request, *args, **kwargs):
        appointment_id = kwargs.get('pk')
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {
                    "message": "Appointment not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AppointmentStatusUpdateSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Appointment status updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Invalid data",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    

class AppointmentPaymentStatusUpdateView(APIView):

    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = [IsAuthenticated | IsPatientManager | IsDoctor ,]

    def patch(self, request, *args, **kwargs):
        appointment_id = kwargs.get('pk')
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response(
                {
                    "message": "Appointment not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AppointmentPaymentStatusUpdateSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Appointment status updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Invalid data",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    

class AppointmentListView(APIView):

    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = [IsDoctor | IsPatientManager | IsBranchAdministrator | IsSuperUser,]

    def get(self, request, doctor_id, format=None):
        today = datetime.now().date()
        appointments = Appointment.objects.filter(
            doctor__id=doctor_id, 
            created_at__date=today
        ).exclude(status__in=['completed', 'canceled']).order_by(
            models.Case(
                models.When(status='critical', then=models.Value(0)),
                models.When(status='in_progress', then=models.Value(1)),
                models.When(status='booked', then=models.Value(2)),
                output_field=models.IntegerField(),
            ),
            'created_at'  
        )
        
        if not appointments.exists():
            return Response([], status=status.HTTP_200_OK)
        
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentListAdminView(APIView):

    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = [IsSuperUser | IsBranchAdministrator | IsPatientManager | IsPatient,]

    def get(self, request):
        appointments = Appointment.objects.exclude(status__in=['completed', 'canceled']).order_by(
            models.Case(
                models.When(status='critical', then=models.Value(0)),
                models.When(status='in_progress', then=models.Value(1)),
                models.When(status='booked', then=models.Value(2)),
                output_field=models.IntegerField(),
            ),
            'created_at'  
        )
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
