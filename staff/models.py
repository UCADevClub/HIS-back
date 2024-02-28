from django.db import models
from user_authentication.models import BaseUser, Address


class Doctor(BaseUser):
    position = models.CharField(max_length=128)
    specialization = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.position} {self.specialization}'
