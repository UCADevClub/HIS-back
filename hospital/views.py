from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication,
)

from .serializers import HospitalSerializer
from .models import Hospital

from hospital.models import (
    Branch,
)
from hospital.serializers import (
    BranchSerializer,
)

from staff.permissions import (
    IsSuperUser,
    IsHospitalAdministrator,
)


class HospitalCreateView(APIView):
    """
    API endpoint for creating and updating hospital data.
    """
    authentication_classes = (
        TokenAuthentication,
    )
    permission_classes = (
        IsSuperUser | IsHospitalAdministrator,
    )

    @staticmethod
    def post(request):
        """
        Creates a new hospital instance.
        """
        hospital_serializer = HospitalSerializer(data=request.data)
        if hospital_serializer.is_valid():
            hospital_serializer.save()
            return Response({
                'message': 'Hospital created successfully',
                'data': hospital_serializer.data
            },
                status=status.HTTP_201_CREATED
            )
        return Response({
            'message': 'Wrong data provided',
            'data': hospital_serializer.errors
        },
            status=status.HTTP_400_BAD_REQUEST)


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
        hospital_id = request.query_params.get('id', )

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


class BranchListCreateAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsHospitalAdministrator | IsSuperUser,)

    @staticmethod
    def get(request):
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Branch created successfully',
                    'data': serializer.data
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                'message': 'Branch not created.',
                'error': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class BranchRetrieveUpdateAPIView(APIView):

    permission_classes = (IsSuperUser,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(branch)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(branch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({'error': 'Branch does not exist'}, status=status.HTTP_404_NOT_FOUND)

        branch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
