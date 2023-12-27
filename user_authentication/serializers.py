from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from user_authentication.models import BaseUser


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'


class BaseUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['individual_unique_number', 'first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = BaseUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
