from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (
    TokenAuthentication
)
from staff.permissions import (
    IsSuperUser,
    IsHospitalAdministrator,
    IsBranchAdministrator,
    IsPatientManager,
)
from staff.serializers import HospitalAdministratorSerializer, BranchAdministratorSerializer
from staff.models import HospitalAdministrator, BranchAdministrator


class HospitalAdministratorSingleView(APIView):
    authentication_classes = (
        TokenAuthentication,
    )

    permission_classes = (
        IsSuperUser | IsHospitalAdministrator,
    )

    @staticmethod
    @swagger_auto_schema(
        responses={
            200: HospitalAdministratorSerializer(),
            401: 'Unauthorized',
            404: 'Hospital administrator not found'
        }
    )
    def get(request, pk):
        hospital_administrator_instance = HospitalAdministrator.objects.filter(
            user_id=pk,
        ).first()
        if hospital_administrator_instance:
            hospital_administrator_serializer = HospitalAdministratorSerializer(hospital_administrator_instance)
            return Response(
                data=hospital_administrator_serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(data={'response': 'hospital administrator not found'}, status=status.HTTP_404_NOT_FOUND)


class HospitalAdministratorView(APIView):
    authentication_classes = (
        TokenAuthentication,
    )

    permission_classes = (
        IsSuperUser | IsHospitalAdministrator,
    )

    @staticmethod
    @swagger_auto_schema(
        responses={
            200: HospitalAdministratorSerializer(many=True),
            401: 'Unauthorized',
            404: 'No hospital administrators found'
        }
    )   
    def get(request, pk):
        hospital_administrator_query = HospitalAdministrator.objects.all()
        if not hospital_administrator_query:
            return Response(data=hospital_administrator_query, status=status.HTTP_200_OK)
        return Response(data={'response': 'hospital administrator is not found'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    @swagger_auto_schema(
        request_body=HospitalAdministratorSerializer,
        responses={
            200:HospitalAdministratorSerializer,
            400: 'Invalid request data'
        }
    )
    def post(request, *args, **kwargs):
        hospital_administrator_serializer = HospitalAdministratorSerializer(
            data=request.data,
        )
        if hospital_administrator_serializer.is_valid():
            hospital_administrator_serializer.save()
            return Response(
                data=hospital_administrator_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            data={'message': hospital_administrator_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class BranchAdministratorView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsSuperUser | IsHospitalAdministrator,)

    @staticmethod
    @swagger_auto_schema(
        request_body=BranchAdministratorSerializer,
        responses={
            200:BranchAdministratorSerializer,
            400: 'Invalid request data'
        }
    )
    def post(request):
        branch_administrator_serializer = BranchAdministratorSerializer(
            data=request.data
        )
        if branch_administrator_serializer.is_valid():
            branch_administrator_serializer.save()
            return Response(
                data={
                    'message': 'BranchAdministrator created successfully',
                    'data': branch_administrator_serializer.data,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={
                'message': 'Incorrect data',
                'data': branch_administrator_serializer.data
            },
            status=status.HTTP_400_BAD_REQUEST
        )