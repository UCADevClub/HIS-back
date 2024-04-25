from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication
)

from .serializers import HospitalSerializer
from .models import Hospital

from staff.permissions import (
    IsSuperUser,
    IsHospitalAdmin,
)

class HospitalCreateView(APIView):
    """
    API endpoint for creating and updating hospital data.
    """
    # authentication_classes = (
    #     SessionAuthentication,
    #     BasicAuthentication,
    # )
    permission_classes = (
        IsAuthenticated,
    )
    def has_permission(self, request, obj=None):
        """
        Custom permission checking for Superuser or HospitalAdministrator.
        """

        if not super().has_permission(request, obj):
            return False

        # Allow access if either IsSuperUser or IsHospitalAdmin permission is granted
        return request.user.is_superuser or IsHospitalAdmin().has_permission(request, obj)

    def post(self, request):
        """
        Creates a new hospital instance.
        """
        serializer = HospitalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hospital = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class HospitalUpdateView(APIView):
    """
    API endpoint for updating hospital data.
    """
    # authentication_classes = (
    #     SessionAuthentication,
    #     BasicAuthentication,
    # )
    permission_classes = (
        IsAuthenticated,
        IsSuperUser,
    )

    def patch(self, request, pk):
        """
        Partially updates an existing hospital instance.
        """
        try:
            hospital = Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HospitalSerializer(hospital, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class HospitalListView(APIView):
    """
    API endpoint for retrieving hospital data.
    """

    def get(self, request):
        """
        Retrieves a list of all hospitals or a single hospital by ID.
        """
        hospital_id = request.query_params.get('id')

        if hospital_id:
            try:
                hospital = Hospital.objects.get(pk=hospital_id)
                serializer = HospitalSerializer(hospital)
                return Response(serializer.data)
            except Hospital.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            hospitals = Hospital.objects.all()
            serializer = HospitalSerializer(hospitals, many=True)
            return Response(serializer.data)