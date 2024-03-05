from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from patient.serializers import (
    PatientSerializer,
    PatientCreateSerializer,
)
from patient.models import (
    Patient,
)


class PatientCreateView(APIView):

    @staticmethod
    @swagger_auto_schema(
        request_body=PatientSerializer,
        responses={
            200: PatientSerializer,
            400: 'Invalid request data'
        }
    )
    def post(request, *args, **kwargs):
        patient_serializer = PatientCreateSerializer(
            data=request.data
        )
        if patient_serializer.is_valid():
            patient_serializer.save()
            return Response(
                data=patient_serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, inn):
        if request.data != inn:
            return Response(data={'response': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        patient_instance = Patient.objects.filter(baseuser_ptr=inn).first()
        if patient_instance:
            patient_serializer = PatientSerializer(patient_instance)
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