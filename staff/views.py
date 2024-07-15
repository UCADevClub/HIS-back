from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (
    TokenAuthentication
)
from staff.permissions import (
    IsAdmin,
    IsSuperUser,
    IsHospitalAdministrator,
    IsBranchAdministrator,
    IsPatientManager,
)
from staff.serializers import HospitalAdministratorSerializer, BranchAdministratorSerializer,DoctorSerializer, PatientManagerSerializer,SpecialitySerializer
from staff.models import HospitalAdministrator, BranchAdministrator,Doctor,PatientManager


class HospitalAdministratorSingleView(APIView):
    authentication_classes = (
        TokenAuthentication,
    )

    permission_classes = (
        IsSuperUser | IsAdmin,
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
                status=status.HTTP_200_OK,
            )
        return Response(data={'response': 'hospital administrator not found'}, status=status.HTTP_404_NOT_FOUND)


class HospitalAdministratorView(APIView):
    authentication_classes = (
        TokenAuthentication,
    )

    permission_classes = (
        IsSuperUser | IsHospitalAdministrator,
    )

    
    @swagger_auto_schema(
        responses={
            200: HospitalAdministratorSerializer(many=True),
            401: 'Unauthorized',
            404: 'No hospital administrators found'
        }
    )   
    def get(self,request):
        hospital_administrator_query = HospitalAdministrator.objects.all()
        if  hospital_administrator_query:
            hospital_administrator_serializer = HospitalAdministratorSerializer(hospital_administrator_query,many=True)
            return Response(data=hospital_administrator_serializer.data, status=status.HTTP_200_OK)
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
#DOCTOR VIEWS
class DoctorCreateView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def post(self, request):
        doctor_serializer = DoctorSerializer(data=request.data)
        if doctor_serializer.is_valid():
            doctor_serializer.save()
            return Response(data={"message": "Doctor Created Successfully",
                                  "data": doctor_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(data={
            "message": "Incorrect data",
            "errors": doctor_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class DoctorListView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)
    
    def get(self,request):
        doctor_query = Doctor.objects.all()
        doctor_query_serializer = DoctorSerializer(doctor_query,many = True)
        if doctor_query_serializer:
            return Response(data=doctor_query_serializer.data, status=status.HTTP_200_OK)
        return Response(data={"message":"Doctors Not Found"}, status=status.HTTP_404_NOT_FOUND)
    

class RetrieveUpdateDeleteDoctor(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)
    
    def get (self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"message": "Method GET not allowed"})
        try:
            instance = Doctor.objects.get(pk=pk)
        except:
            return Response({"message":"Object does not exist"})
        doctor_serializer = DoctorSerializer(instance)
        return Response(data=doctor_serializer.data, status=status.HTTP_200_OK)
    
    def put (self, request,*args,**kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"message":"Method PUT not allowed"})
        try:
            instance = Doctor.objects.get(pk=pk)
        except:
            return Response({"message":"Object does not exist"})
        doctor_serializer = DoctorSerializer(instance,data=request.data)
        if doctor_serializer.is_valid():
            doctor_serializer.save()
            return Response(data={"message":"Doctor successfully updated","data":doctor_serializer.data}, status=status.HTTP_200_OK)
        return Response(data=doctor_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"message": "Method GET not allowed"})
        try:
            instance = Doctor.objects.get(pk=pk)
        except:
            return Response({"message":"Object does not exist"})
        doctor_serializer = DoctorSerializer(instance,data=request.data,partial = True)
        if doctor_serializer.is_valid():
            doctor_serializer.save()
            return Response(data={"message":"Doctor successfully updated","data":doctor_serializer.data}, status=status.HTTP_200_OK)
        return Response(data=doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            instance = Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return Response({'message': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorSearch(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)
    
    def get(self, request, *args, **kwargs):
        name = request.query_params.get('name', None)
        if not name:
            return Response({"message": "Please provide a name parameter for searching"}, status=status.HTTP_400_BAD_REQUEST)
        
        doctors = Doctor.objects.filter(first_name__icontains=name) | Doctor.objects.filter(last_name__icontains=name)
        serializer = DoctorSerializer(doctors, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
#PatientManager VIEWS
class PatientManagerCreateView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def post(self,request):
        patinet_manager_serializer = PatientManagerSerializer(data=request.data)
        if patinet_manager_serializer.is_valid():
            patinet_manager_serializer.save()
            return Response(data={
                "message":"Patient manager created successfully",
                "data":patinet_manager_serializer.data},status=status.HTTP_201_CREATED
            )
        return Response(data={
            "errors":patinet_manager_serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    

class PatientManagerListView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def get(self,request):
        patient_manager_query = PatientManager.objects.all()
        if patient_manager_query:
            patient_manager_serializer = PatientManagerSerializer(patient_manager_query, many=True)
            return Response(data=patient_manager_serializer.data, status=status.HTTP_200_OK)
        return Response(data={"message":"Objects not found"},status=status.HTTP_404_NOT_FOUND)


class PatientManagerRetrieveUpdateDelete(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsBranchAdministrator,)

    def get (self,request,pk):
        patient_manager_query = PatientManager.objects.get(pk=pk)
        if patient_manager_query:
            patient_manager_serializer = PatientManagerSerializer(patient_manager_query)
            return Response(data=patient_manager_serializer.data,status=status.HTTP_200_OK)
        return Response(data={"message":"PatientManager not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request,pk):
        patient_manager_query= PatientManager.objects.get(pk=pk)
        if patient_manager_query:
            patient_manager_serializer = PatientManagerSerializer(patient_manager_query,data=request.data)
            if patient_manager_serializer.is_valid():
                patient_manager_serializer.save()
                return Response(data={"message":"Patient Manager updated successfully","data":patient_manager_serializer.data}, status=status.HTTP_200_OK)
            return Response(data=patient_manager_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Patient Manager Not Found"},status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        patient_manager_query= PatientManager.objects.get(pk=pk)
        if patient_manager_query:
            patient_manager_serializer = PatientManagerSerializer(patient_manager_query,data=request.data, partial=True)
            if patient_manager_serializer.is_valid():
                patient_manager_serializer.save()
                return Response(data={"message":"Patient Manager updated successfully","data":patient_manager_serializer.data}, status=status.HTTP_200_OK)
            return Response(data=patient_manager_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Patient Manager Not Found"},status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,pk):
        try:
            instance = PatientManager.objects.get(pk=pk)
        except PatientManager.DoesNotExist:
            return Response({'message': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Speciality VIEWS
class SpecialityCreateAPIView(APIView):
    def post(self, request):
        serializer = SpecialitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)