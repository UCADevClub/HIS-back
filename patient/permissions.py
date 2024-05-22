from rest_framework.permissions import BasePermission
from patient.models import (
    Patient,
)


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_patient
