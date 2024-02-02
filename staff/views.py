from django.shortcuts import render
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

# Create your views here.
