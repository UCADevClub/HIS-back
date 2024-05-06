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
from staff.serializers import HospitalAdministratorSerializer
from staff.models import HospitalAdministrator


class HospitalAdministratorSingleView(APIView):
    authentication_classes = (
        TokenAuthentication,
    )

    permission_classes = (
        IsSuperUser | IsHospitalAdministrator,
    )

    @staticmethod
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
    def get(request, pk):
        hospital_administrator_query = HospitalAdministrator.objects.all()
        if not hospital_administrator_query:
            return Response(data=hospital_administrator_query, status=status.HTTP_200_OK)
        return Response(data={'response': 'hospital administrators not found'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
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
