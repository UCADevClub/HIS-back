from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import (
    TokenAuthentication,
)

from .serializers import HospitalSerializer, AllergySerializer, VaccineSerializer, PillSerializer
from .models import Hospital, Allergy, Vaccine, Pill

from hospital.models import (
    Branch,
)
from hospital.serializers import (
    BranchSerializer,
)

from staff.permissions import (
    IsAdmin,
    IsSuperUser,
    IsHospitalAdministrator,
    IsBranchAdministrator,
)

# !HOSPITAL  VIEWS
class HospitalCreateView(APIView):
    """
    API endpoint for creating and updating hospital data.
    """
    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = (
            IsAdmin | IsSuperUser,
    )

    @staticmethod
    @swagger_auto_schema(
        request_body=HospitalSerializer,
        responses={
            200: HospitalSerializer,
            400: 'Invalid request data'
        }
    )
    
    def post(request):
        """
        Creates a new hospital instance.
        """
        hospital_serializer = HospitalSerializer(data=request.data)
        print(hospital_serializer)
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
    permission_classes = (
        IsAuthenticated, 
        IsHospitalAdministrator | IsSuperUser,
        )

    @swagger_auto_schema(
        request_body=HospitalSerializer,
        responses={
            200: HospitalSerializer,
            400: 'Invalid request data',
            403: 'Permission denied: User cannot update this hospital'
        }
    )
    def patch(self, request, pk):
        """
        Partially updates an existing hospital instance.
        """
        user = request.user

        try:
            hospital = Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if user ID matches hospital administrator's user ID
        if user.user_id != hospital.hospital_administrator.user_id and not IsSuperUser:
            return Response({'message': 'Permission denied: User cannot update this hospital'}, status=status.HTTP_403_FORBIDDEN)
        else:
            # Check if request body contains any update data
            if not request.data:
                return Response({'message': 'No update data provided'}, status=status.HTTP_409_CONFLICT)
            else:
                serializer = HospitalSerializer(hospital, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({
                    'message': 'Hospital updated successfully',
                    'data': serializer.data
                    },
                status=status.HTTP_200_OK
                )
                

class HospitalListView(APIView):
    """
    API endpoint for retrieving hospital data.
    """
    
    @swagger_auto_schema(
        responses={
            200: HospitalSerializer,
            401: 'Unauthorized',
            404: 'Hospital not found'
        }
    )
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

# !BRANCH VIEWS
class BranchCreateView(APIView):
    authentication_classes = (
            TokenAuthentication,
    )
    permission_classes = (
            IsHospitalAdministrator | IsSuperUser,
    )

    @staticmethod
    @swagger_auto_schema(
        request_body=BranchSerializer,
        responses={
            200:BranchSerializer,
            400:'Invalid request data'

        }
    )

    @staticmethod
    @swagger_auto_schema(
        request_body= BranchSerializer,
        responses={
            200:BranchSerializer,
            400:'Invalid request data'
        }
    )
    def post(request):
        branch_serializer = BranchSerializer(data=request.data)
        if branch_serializer.is_valid():
            branch_serializer.save()
            return Response(
                data={
                        'message': 'Branch created successfully',
                        'data': branch_serializer.data,
                },
                status=status.HTTP_201_CREATED

            )
        return Response(
            data={
                    'message': 'Invalid data provided',
                    'data': branch_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,

        )

class BranchUpdateView(APIView):
    """
    API endpoint for updating hospital branch data.
    """
    permission_classes = (
        IsAuthenticated,
        IsBranchAdministrator | IsSuperUser,
    )

    @swagger_auto_schema(
        request_body=BranchSerializer,
        responses={
            200: BranchSerializer,
            400: 'Invalid request data',
            403: 'Permission denied: User cannot update this hospital`s branch'
        }
    )
    def patch(self, request, pk):
        try:
            branch_instance = Branch.objects.filter(id=pk).first()
            if not branch_instance:
                return Response(
                    data={
                        'message': f'Branch with id={pk} does not exist',
                        'data': {},
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            branch_serializer = BranchSerializer(
                branch_instance,
                data=request.data,
                partial=True,
            )
            if branch_serializer.is_valid():
                branch_serializer.save()
                return Response(
                    data={
                        'message': 'Updated successfully',
                        'data': branch_serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                data={
                    'message': 'Invalid data provided',
                    'errors': branch_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            return Response(
                data={
                    'message': 'Validation error',
                    'errors': e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class BranchListAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsHospitalAdministrator | IsSuperUser,)

    @staticmethod
    @swagger_auto_schema(
        responses={
            200: BranchSerializer,
            401: 'Unauthorized',
            404: 'Branch not found'
        }
    )
    
    def get(request):
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)

    # @staticmethod
    # @swagger_auto_schema(
    #     request_body=BranchSerializer,
    #     responses={
    #         200:BranchSerializer,
    #         400: 'Invalid request data'
    #     }
    # )
    # def post(request):
    #     serializer = BranchSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             {
    #                     'message': 'Branch created successfully',
    #                     'data': serializer.data
    #             },
    #             status=status.HTTP_201_CREATED
    #         )
    #     return Response(
    #         {
    #                 'message': 'Branch not created.',
    #                 'error': serializer.errors,
    #         },
    #         status=status.HTTP_400_BAD_REQUEST
    #     )


class BranchRetrieveUpdateAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsSuperUser | IsHospitalAdministrator,)

    @swagger_auto_schema(
        responses={
            200: BranchSerializer,
            404: 'Branch not found'
        }
    )

    def get(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({'message': 'Branch does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(branch)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({'message': 'Branch does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(branch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @swagger_auto_schema(
        request_body= BranchSerializer,
        responses={
            200: BranchSerializer,
            400: 'Invalid request data'
        }
    )
    def patch(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({'message': 'Branch does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
    @swagger_auto_schema(
        request_body=BranchSerializer,
        responses={
            204: 'Branch deleted successfully',
            404: 'Branch not found'
        }
    )
    def delete(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({'message': 'Branch does not exist'}, status=status.HTTP_404_NOT_FOUND)

        branch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Allergy VIEWS
class AllergyCreateView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def post(self,request):
        allergy_serializer = AllergySerializer(data=request.data)
        if allergy_serializer.is_valid():
            allergy_serializer.save()
            return Response(data={"message":"Allergy created successfully","data":allergy_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(data=allergy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllergyListView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def get (self,request):
        allergy_query = Allergy.objects.all()
        if allergy_query:
            allergy_serializer = AllergySerializer(allergy_query,many = True)
            return Response(data=allergy_serializer.data, status=status.HTTP_200_OK)
        return Response({"message":"Allergy not found"}, status=status.HTTP_404_NOT_FOUND)
    

class AllergyRetrieveUpdateDelete(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)
    
    def get (self,request,pk):
        allergy_query = Allergy.objects.get(pk=pk)
        if allergy_query:
            allergy_seriazlizer = AllergySerializer(allergy_query)
            return Response(data=allergy_seriazlizer.data, status=status.HTTP_200_OK)
        return Response(data={"message":"Allergy not found"},status=status.HTTP_404_NOT_FOUND)
    
    def put (self,request,pk):
        allergy_query = Allergy.objects.get(pk=pk)
        if allergy_query:
            allergy_serializer = AllergySerializer(allergy_query,data=request.data)
            if allergy_serializer.is_valid():
                allergy_serializer.save()
                return Response(data={"message":"Allergy updated successfully","data":allergy_serializer.data},status=status.HTTP_200_OK)
            return Response(data=allergy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message":"Allergy not found"},status=status.HTTP_404_NOT_FOUND)
    
    def patch (self,request,pk):
        allergy_query = Allergy.objects.get(pk=pk)
        if allergy_query:
            allergy_serializer = AllergySerializer(allergy_query, data=request.data, partial = True)
            if allergy_serializer.is_valid():
                allergy_serializer.save()
                return Response(data={"message":"Allergy updated successfully","data":allergy_serializer.data},status=status.HTTP_200_OK)
            return Response(data=allergy_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message":"Allergy not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete (self,request,pk):
        try: 
            allergy_query = Allergy.objects.get(pk=pk)
        except Allergy.DoesNotExist:
            return Response(data={"message":"Allergy does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        allergy_query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#Vaccine VIEWS
class VaccineCreateView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def post (self,request):
        vaccine_serializer = VaccineSerializer(data=request.data)
        if vaccine_serializer.is_valid():
            vaccine_serializer.save()
            return Response(data={"message":"Vaccine created successfully","data":vaccine_serializer.data},status=status.HTTP_201_CREATED)
        return Response(data=vaccine_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VaccineListView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def get(self,rquest):
        vaccine_query = Vaccine.objects.all()
        if vaccine_query:
            vaccine_serializer = VaccineSerializer(vaccine_query, many = True)
            return Response(data=vaccine_serializer.data, status=status.HTTP_200_OK)
        return Response(data={"message":"Vaccine not found"}, status=status.HTTP_404_NOT_FOUND)


class VaccineRetrieveUpdateDelete(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def get(self,request,pk):
        vaccine_query = Vaccine.objects.get(pk=pk)
        if vaccine_query:
            vaccine_serializer = VaccineSerializer(vaccine_query)
            return Response(data=vaccine_serializer.data, status=status.HTTP_200_OK)
        return Response(data={"message":"Vaccine not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        vaccine_query = Vaccine.objects.get(pk=pk)
        if vaccine_query:
            vaccine_serializer = VaccineSerializer(vaccine_query,data=request.data)
            if vaccine_serializer.is_valid():
                vaccine_serializer.save()
                return Response(data={"message":"Vaccine updated successfully","data":vaccine_serializer.data}, status=status.HTTP_200_OK)
            return Response(data=vaccine_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message":"Vaccine not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self,request,pk):
        vaccine_query = Vaccine.objects.get(pk=pk)
        if vaccine_query:
            vaccine_serializer = VaccineSerializer(vaccine_query,data=request.data, partial = True)
            if vaccine_serializer.is_valid():
                vaccine_serializer.save()
                return Response(data={"message":"Vaccine updated successfully","data":vaccine_serializer.data}, status=status.HTTP_200_OK)
            return Response(data=vaccine_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message":"Vaccine not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,pk):
        try:
            vaccine_query = Vaccine.objects.get(pk=pk)
        except Vaccine.DoesNotExist:
            return Response(data={"message":"Vaccine does not exist"},status=status.HTTP_404_NOT_FOUND)
        
        vaccine_query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#Pill VIEWS
class PillCreateView(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def post(self,request):
        pill_serializer = PillSerializer(data=request.data)
        if pill_serializer.is_valid():
            pill_serializer.save()
            return Response(data={"message":"Pill created successfully","data":pill_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(data=pill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PillListView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def get(self,request):
        pill_query = Pill.objects.all()
        if pill_query:
            pill_serializer = PillSerializer(pill_query, many= True)
            return Response(data=pill_serializer.data, status=status.HTTP_200_OK)
        return Response(data={"message":"Pill not found"},status=status.HTTP_404_NOT_FOUND)


class PillRetrieveUpdateDelete(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def get(self,request,pk):
        pill_query = Pill.objects.get(pk=pk)
        if pill_query:
            pill_serializer = PillSerializer(pill_query)
            return Response(data=pill_serializer.data, status=status.HTTP_200_OK)
        return Response(data={"message":"Pill not found"},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,pk):
        pill_query = Pill.objects.get(pk=pk)
        if pill_query:
            pill_serializer = PillSerializer(pill_query, data=request.data)
            if pill_serializer.is_valid():
                pill_serializer.save()
                return Response(data={"message":"Pill updated successfully","data":pill_serializer.data}, status=status.HTTP_200_OK)
            return Response(data=pill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"Pill not found"},status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,pk):
        pill_query = Pill.objects.get(pk=pk)
        if pill_query:
            pill_serializer = PillSerializer(pill_query, data=request.data, partial = True)
            if pill_serializer.is_valid():
                pill_serializer.save()
                return Response(data={"message":"Pill updated successfully","data":pill_serializer.data}, status=status.HTTP_200_OK)
            return Response(data=pill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"Pill not found"},status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,pk):
        try:
            pill_query = Pill.objects.get(pk=pk)
        except Pill.DoesNotExist:
            return Response(data={"Pill not found"},status=status.HTTP_404_NOT_FOUND)
        
        pill_query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

        



    

        
