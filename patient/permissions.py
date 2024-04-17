from rest_framework.permissions import BasePermission
from patient.models import (
    Patient,
    EmergencyContact
)


class PatientPermission(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Patient)
