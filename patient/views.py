from .models import EmergencyContact, Patient
from .serializers import EmergencyContactSerializer, PatientSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

# ------------- Emergency Contact -------------
class EmergencyContactList(ListCreateAPIView):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer

class EmergencyContactDetail(RetrieveUpdateDestroyAPIView):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer

# ------------- Patient -------------

class PatientList(ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientDetail(RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer