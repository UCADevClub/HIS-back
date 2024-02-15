from rest_framework import status
from django.http import Http404

from patient.serializers import PatientSerializer
from patient.models import Patient

from rest_framework.views import APIView
from rest_framework.response import Response


def get_patient_object(inn):
    try:
        return Patient.objects.get(inn=inn)
    except Patient.DoesNotExist:
        raise Http404(f"Patient with {inn} inn not found")


class PatientDetail(APIView):

    def get(self, request, inn):
        try:
            patient_instance = get_patient_object(inn=inn)
            patient_serializer = PatientSerializer(patient_instance)
            return Response(patient_serializer.data, status=status.HTTP_200_OK)
        except Http404 as error:
            return Response(data={f'{error=}'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, inn):
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


