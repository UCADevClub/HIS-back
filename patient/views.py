from rest_framework import status
from django.http import Http404

from patient.serializers import (
    PatientSerializer,
    PatientCreateSerializer,
    EmergencyContactCreateSerializer
)
from patient.models import (
    Patient,
    EmergencyContact,
)

from user_authentication.models import BaseUser
from user_authentication.serializers import BaseUserCreateSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.views.generic.detail import DetailView


def get_patient_object(inn):
    try:
        return Patient.super().objects.get(baseuser_id=inn)
    except Patient.DoesNotExist:
        raise Http404(f"Patient with {inn} inn not found")


class PatientCreateView(APIView):

    @staticmethod
    def post(request):
        try:
            patient_serializer = PatientCreateSerializer(data=request.data)
            if patient_serializer.is_valid(raise_exception=True):
                patient_serializer.save()
                return Response(data=patient_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            print(error.detail)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(APIView):

    def get(self, request, inn, format=None):
        patient = Patient.objects.filter(inn=inn).first()
        if patient:
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        else:
            return Response({"detail": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def patch(request, inn):
        try:
            patient_instance = get_patient_object(inn=inn)
            patient_serializer = PatientSerializer(patient_instance, data=request.data, partial=True)
            if patient_serializer.is_valid():
                print(f"Patient {patient_instance.first_name} {patient_instance.last_name} created successfully!")
                patient_serializer.save()
                return Response(patient_serializer.data, status=status.HTTP_200_OK)
            return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as error:
            return Response(data={f'{error=}'}, status=status.HTTP_404_NOT_FOUND)


class PatientList(APIView):

    @staticmethod
    def get(request):
        patient_instance = Patient.objects.all()
        patient_serializer = PatientSerializer(patient_instance, many=True)
        return Response(patient_serializer.data, status=status.HTTP_200_OK)


