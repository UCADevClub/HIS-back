from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from djoser.urls.base import User


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class BaseUser(User):
    individual_unique_number = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    GENDER_CHOICES = [
            ('M', 'Male'),
            ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    date_of_birth = models.DateField()

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
