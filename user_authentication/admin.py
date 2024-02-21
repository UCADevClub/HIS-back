from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Address, BaseUser


class CustomAdminManager(UserAdmin):
    fieldsets = (
            (None, {'fields': ('email', 'password')}),
            ('Personal info', {'fields': ('inn', 'first_name', 'last_name', 'date_of_birth', 'gender')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'groups', 'user_permissions')}),
    )


admin.site.register(Address)
admin.site.register(BaseUser)
