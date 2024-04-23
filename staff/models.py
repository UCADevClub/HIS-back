from django.db import models
from user_authentication.models import StandardUser, BaseUser
from hospital.models import Department


class Speciality(models.Model):
    position = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return self.position


class Doctor(StandardUser):
    is_staff = True
    speciality = models.OneToOneField(
        Speciality,
        on_delete=models.CASCADE,
        related_name='speciality',
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='department',
    )
    is_branch_director = models.BooleanField(default=False)
    is_department_director = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name} {self.speciality}'


class BranchAdministrator(BaseUser):
    is_manager = True
    is_staff = True


class HospitalManager(BranchAdministrator):
    is_admin = True
