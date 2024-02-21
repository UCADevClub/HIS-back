from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, inn, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)

        if not password:
            password = make_password(password=None)

        user = self.model(email=email, inn=inn, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, inn, password=None, **extra_fields):
        user = self.create_user(email=email, inn=inn, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser, PermissionsMixin):
    inn = models.CharField(unique=True, primary_key=True, max_length=64)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128, unique=True)
    date_of_birth = models.DateField(null=True)
    password = models.CharField(max_length=128, default=inn)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    GENDER_CHOICES = [
            ('M', 'Male'),
            ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "inn"]

    def __str__(self):
        return f'User: {self.first_name} {self.last_name} {self.middle_name}'


class Address(models.Model):
    country = models.CharField(max_length=128)
    oblast = models.CharField(max_length=128)
    city_village = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    house = models.CharField(max_length=128)
    apartment = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.street}, {self.house}, {self.country} {self.oblast}"

