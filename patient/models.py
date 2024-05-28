from django.db import models
from user_authentication.models import StandardUser


class Patient(StandardUser):
    is_patient = True

    class Meta:
        db_table = 'Patient'