from datetime import datetime
from django.db import models, IntegrityError, transaction
from patient.models import Patient
from staff.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Ожидание приема'),
        ('in_progress', 'На приеме'),
        ('completed', 'Выписан'),
        ('canceled', 'Отменен'),
        ('critical', 'Критический'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('not_paid', 'Not Paid'),
        ('paid', 'Paid'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True)
    referral_doctor = models.ForeignKey(Doctor, related_name='referral_appointments', on_delete=models.SET_NULL,
                                        blank=True, null=True)
    talon = models.CharField(max_length=10, unique=True, blank=True)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='not_paid')
    is_referral = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.talon:
            with transaction.atomic():
                self.talon = self.generate_unique_talon()
        super().save(*args, **kwargs)

    def generate_unique_talon(self):
        speciality_initial = ''.join([s.position[0].upper() for s in self.doctor.speciality.all()[:1]])
        today = datetime.now().date()

        # Use a transaction to ensure uniqueness
        with transaction.atomic():
            count = Appointment.objects.filter(
                doctor=self.doctor,
                created_at__date=today
            ).count()

            # Ensure sequential_number is three digits long
            sequential_number = str(count + 1).zfill(3)
            talon = f"{speciality_initial}{sequential_number}"

            # Ensure the talon is unique
            while Appointment.objects.filter(talon=talon).exists():
                count += 1
                sequential_number = str(count + 1).zfill(3)
                talon = f"{speciality_initial}{sequential_number}"

                if count > 999:  # Adjust this if you expect more than 999 appointments per day
                    raise IntegrityError("Unable to generate a unique talon after multiple attempts.")

            return talon


    def __str__(self):
        return f"Appointment with Dr. {self.doctor} for {self.patient} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
