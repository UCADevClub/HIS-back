from django.db import models


class InsuranceInfoTable(models.Model):
    health_insurance_name = models.CharField(max_length=64)
    insurance_policy_id = models.IntegerField()
    insurance_package_type = models.CharField()


class MedicalData(models.Model):
    choice_glasses_contact_lenses = (
            ('YWG', 'Wears Glasses'),
            ('YWCL', 'Wears Contact Lenses'),
            ('N', 'No')
    )

    blood_type = models.CharField(max_length=64)
    glasses_contact_lenses = models.CharField(max_length=64, choices=choice_glasses_contact_lenses, default='N')
    vaccination_status = models.CharField(max_length=128)
    allergies = models.CharField(max_length=512)
    medicine = models.CharField(max_length=512)
    other_health_issues = models.CharField(max_length=512)
