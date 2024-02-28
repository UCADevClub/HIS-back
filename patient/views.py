from rest_framework import status
from django.http import Http404

from patient.serializers import (
    PatientSerializer,
    PatientCreateSerializer,
)
from patient.models import (
    Patient,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class PatientCreateView(APIView):

    @staticmethod
    def post(request):
        patient_serializer = PatientCreateSerializer(data=request.data)
        print(patient_serializer.is_valid(), request.data)
        if patient_serializer.is_valid():
            patient_serializer.save()
            return Response(data=patient_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(APIView):
    # permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, inn):
        patiet_instance = Patient.objects.filter(baseuser_ptr=inn).first()
        if patiet_instance:
            patient_serializer = PatientSerializer(patiet_instance)
            return Response(data=patient_serializer.data, status=status.HTTP_200_OK)
        return Response(data={'response: ': 'patient not found'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def patch(request, inn):
        try:
            patient_instance = Patient.objects.filter(baseuser_ptr=inn).first()
            patient_serializer = PatientSerializer(patient_instance, data=request.data, partial=True)
            if patient_serializer.is_valid():
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
