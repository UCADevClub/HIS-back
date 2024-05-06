from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsHospitalAdministrator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_hospital_administrator


class IsBranchAdministrator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_branch_administrator


class IsPatientManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_patient_manager
