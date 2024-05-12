from django.contrib import admin
from .models import Address, StandardUser, BaseUser

admin.site.register(BaseUser)
admin.site.register(StandardUser)
admin.site.register(Address)
