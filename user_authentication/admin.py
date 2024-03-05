from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Address, BaseUser

admin.site.register(Address)
admin.site.register(BaseUser)
