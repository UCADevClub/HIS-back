from django.shortcuts import render
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

# Create your views here.
class DoctorList(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorDetail(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer