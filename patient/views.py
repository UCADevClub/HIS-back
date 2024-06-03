from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication, TokenAuthentication
)

from patient.serializers import (
    PatientSerializer,
)
from patient.models import (
    Patient,
)
from patient.permissions import (
    IsPatient
)
from staff.permissions import (
    IsPatientManager,
)


class PatientCreateView(APIView):
    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = (
        IsPatientManager,
    )

    @staticmethod
    @swagger_auto_schema(
        request_body=PatientSerializer,
        responses={
            200: PatientSerializer,
            400: 'Invalid request data'
        }
    )
    def post(request, *args, **kwargs):
        patient_serializer = PatientSerializer(
            data=request.data
        )
        if patient_serializer.is_valid():
            patient_serializer.save()
            return Response(
                data=patient_serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=patient_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(APIView):
    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = (
            IsPatientManager | IsPatient,
    )

    @staticmethod
    @swagger_auto_schema(
        responses={
            200: PatientSerializer,
            401: 'Unauthorized',
            404: 'Patient not found'
        }
    )
    def get(request, inn):
        patient_instance = Patient.objects.filter(
            baseuser_ptr=inn,
        ).first()
        if patient_instance:
            patient_serializer = PatientSerializer(patient_instance)
            return Response(
                data=patient_serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(data={'response: ': 'patient not found'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    @swagger_auto_schema(
        request_body=PatientSerializer,
        responses={
            200: PatientSerializer,
            400: 'Invalid request data'
        }
    )
    def patch(request, user_id):
        try:
            patient_instance = Patient.objects.filter(baseuser_ptr=user_id).first()
            patient_serializer = PatientSerializer(
                patient_instance, data=request.data, partial=True)
            if patient_serializer.is_valid():
                patient_serializer.save()
                return Response(patient_serializer.data, status=status.HTTP_200_OK)
            return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as error:
            return Response(data={f'{error=}'}, status=status.HTTP_404_NOT_FOUND)


class PatientList(APIView):

    authentication_classes = (
            TokenAuthentication,
    )

    @staticmethod
    @swagger_auto_schema(
        responses={
            200: PatientSerializer,
            401: 'Unauthorized',
            404: 'Patient not found'
        }
    )
    def get(request):
        patient_instance = Patient.objects.all()
        patient_serializer = PatientSerializer(patient_instance, many=True)
        return Response(patient_serializer.dgata, status=status.HTTP_200_OK)


class PatientSearch(APIView):
    """
        An APIView for searching Patient objects based on either full name or INN (Individual Taxpayer Number).

        Handles GET requests to search for patients using a single query parameter named 'name'. 
        The length of the query parameter should be more than 1 character.

        The search can be performed by:
            - Full name (space-separated first and last name): Supports partial matching in both names.
            - INN (digits only): Filters patients based on their INN number (case-insensitive).
        
        Query Parameters:
            - name (str): A full name or user_id to search for.
                -Example: 
                    1) GET http://request/?name=John Smith
                    2) GET http://request/?name=John
                    3) GET http://request/?name=Smith
                    4) GET http://request/?name=22512199945678            

        Response:
            A JSON response containing a list of matching Patient objects, serialized using PatientSerializer.
            - 200 (OK): Returned if patients are found matching the search criteria.
            - 404 (Not Found): Raised if no patients match the search criteria.
    """

    @staticmethod
    @swagger_auto_schema(
        responses={
            200: PatientSerializer,
            401: 'Unauthorized',
            404: 'Patient not found'
        }
    )
    def get(request):

        full_name_or_inn = request.query_params.get('name', )

        if full_name_or_inn.isdigit():
            inn = full_name_or_inn
            query = Q(inn__icontains=inn)
        else:
            inn = None
            names = full_name_or_inn.split(" ")
            first_name = names[0]
            last_name = names[-1] if len(names) > 1 else ""

            query = Q()

            if first_name and last_name:
                # If both first name and last name are provided, only include records
                # where both names match
                query |= (Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name)) | (Q(first_name__icontains=last_name) & Q(last_name__icontains=first_name))
            else:
                if first_name:
                    # Check if the first name matches either first_name or last_name column
                    query |= Q(first_name__icontains=first_name) | Q(last_name__icontains=first_name)
                if last_name:
                    # Check if the last name matches either first_name or last_name column
                    query |= Q(first_name__icontains=last_name) | Q(last_name__icontains=last_name)

        results = Patient.objects.filter(query)

        if not results:
            raise Http404("No matching patients found")

        serializer = PatientSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)