from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EmergencyContact, Patient
from .serializers import EmergencyContactSerializer, PatientSerializer
from user_authentication.serializers import AddressSerializer
from user_authentication.models import Address


# ------------- Emergency Contact -------------

@csrf_exempt
@require_http_methods(["POST"])
def create_emergency_contact(request):
    serializer = EmergencyContactSerializer(data=request.POST)
    if serializer.is_valid():
        emergency_contact = serializer.save()
        return JsonResponse({"status": "success", "contact_id": emergency_contact.pk})
    return JsonResponse({"status": "error", "errors": serializer.errors}, status=400)


@csrf_exempt
@require_http_methods(["PUT"])
def edit_emergency_contact(request, contact_id):
    emergency_contact = get_object_or_404(EmergencyContact, pk=contact_id)
    serializer = EmergencyContactSerializer(emergency_contact, data=request.data)
    if serializer.is_valid():
        emergency_contact = serializer.save()
        return JsonResponse({"status": "success", "contact_id": emergency_contact.pk})
    return JsonResponse({"status": "error", "errors": serializer.errors}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_emergency_contact(request, contact_id):
    emergency_contact = get_object_or_404(EmergencyContact, pk=contact_id)
    emergency_contact.delete()
    return JsonResponse({"status": "success"})


@csrf_exempt
@require_http_methods(["GET"])
def get_emergency_contact(request, contact_id):
    emergency_contact = get_object_or_404(EmergencyContact, pk=contact_id)
    serializer = EmergencyContactSerializer(emergency_contact)
    return Response(serializer.data)


# ------------- Patient -------------

@csrf_exempt
@require_http_methods(["POST"])
def create_patient(request):
    if request.method == 'POST':
        serializer = PatientSerializer(data=request.POST)
        if serializer.is_valid():
            patient = serializer.save()
            return JsonResponse({"status": "success", "patient_id": patient.pk})
        else:
            return JsonResponse({"status": "error", "errors": serializer.errors}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "GET request not supported for this endpoint"}, status=405)


@csrf_exempt
@require_http_methods(["PUT"])
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    serializer = PatientSerializer(patient, data=request.data)
    if serializer.is_valid():
        patient = serializer.save()
        return JsonResponse({"status": "success", "patient_id": patient.pk})
    return JsonResponse({"status": "error", "errors": serializer.errors}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    patient.delete()
    return JsonResponse({"status": "success"})


@csrf_exempt
@require_http_methods(["GET"])
def get_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    serializer = PatientSerializer(patient)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def get_all_patients(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return JsonResponse(serializer.data, safe=False)
