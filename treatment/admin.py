from django.contrib import admin
from .models import ObjectiveExamination, Treatment, Referral, Medications

admin.site.register(ObjectiveExamination)
admin.site.register(Treatment)
admin.site.register(Referral)
admin.site.register(Medications)