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
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin
    
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_doctor
    def has_object_permission(self, request, view, obj):
        if not request.user.is_doctor:
            return False

        allowed_fields = {'vaccines', 'allergies', 'vision', 'blood_group'}
        if request.method in ['PATCH', 'PUT']:
            data_keys = set(request.data.keys())
            if data_keys.issubset(allowed_fields):
                return True
            return False

        return True