from django.db import models
from user_authentication.models import BaseUser, Address


class Doctor(models.Model):
    doctor: BaseUser = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='emergency_contacts')
    position = models.CharField(max_length=128)
    specialization = models.CharField(max_length=128)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address', null=True)

    def __str__(self):
        return f'{self.doctor} {self.position} {self.specialization}'
