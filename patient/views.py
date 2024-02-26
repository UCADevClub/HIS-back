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


def get_patient_object(inn):
    try:
        return get(baseuser_id=inn)
    except Patient.DoesNotExist:
        raise Http404(f"Patient with {inn} inn not found")


class PatientCreateView(APIView):

    @staticmethod
    def post(request):
        patient_serializer = PatientCreateSerializer(data=request.data)
        if patient_serializer.is_valid():
            patient_serializer.save()
            return Response(data=patient_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


def get(request, inn):
    patient = Patient.objects.filter(inn=inn).first()
    if patient:
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    else:
        return Response({"detail": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)


class PatientDetail(APIView):

    @staticmethod
    def patch(request, inn):
        try:
            patient_instance = get_patient_object(inn=inn)
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
