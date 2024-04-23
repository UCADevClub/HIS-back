from django.db import models
from user_authentication.models import StandardUser


class Patient(StandardUser):
    MARITAL_OPTIONS = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
        ('divorced', 'Divorced'),
        ('common_law', 'Common-Law')
    )

    marital_status = models.CharField(
        max_length=64,
        choices=MARITAL_OPTIONS,
        default='single',
    )

