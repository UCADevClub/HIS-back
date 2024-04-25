from django.contrib import admin
from .models import Hospital, Branch, BranchAddress, BranchPhoneNumber, Department

admin.site.register(Hospital)
admin.site.register(Branch)
admin.site.register(BranchAddress)
admin.site.register(BranchPhoneNumber)
admin.site.register(Department)