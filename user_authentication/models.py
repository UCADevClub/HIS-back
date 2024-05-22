from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from user_authentication.mail.mail import send_password
from django.utils.crypto import get_random_string


class Address(models.Model):
    country = models.CharField(max_length=128)
    oblast = models.CharField(max_length=128)
    city_village = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    house = models.CharField(max_length=128)
    apartment = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.street}, {self.house}, {self.country}, {self.oblast}"


class EmergencyContact(models.Model):
    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if password is None:
            password = get_random_string(8)
            send_password(password=password, targets=[email])
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_patient_manager(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_patient_manager', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email=email, password=password, **extra_fields)

    def create_branch_administrator(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_branch_administrator', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email=email, password=password, **extra_fields)

    def create_hospital_administrator(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_hospital_administrator', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email=email, password=password, **extra_fields)

    def create_patient(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_patient', True)
        return self.create_user(email=email, password=password, **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(unique=True, max_length=64)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128, unique=True)
    password = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_patient_manager = models.BooleanField(default=False)
    is_branch_administrator = models.BooleanField(default=False)
    is_hospital_administrator = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'middle_name', 'user_id')

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'


class StandardUser(BaseUser):
    citizenship = models.CharField(max_length=64)
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=128)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        related_name='standard_user',
        null=True
    )
    primary_emergency_contact = models.ForeignKey(
        EmergencyContact,
        on_delete=models.CASCADE,
        related_name='primary_emergency_contacts',
    )
    secondary_emergency_contact = models.ForeignKey(
        EmergencyContact,
        on_delete=models.CASCADE,
        related_name='secondary_emergency_contacts',
        null=True,
        blank=True,
    )
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
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

