from models import BaseUser

from djoser.serializers import UserCreateSerializer, UserSerializer


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'individual_unique_number', 'phone_number',
                  'date_of_birth', 'gender')


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = BaseUser
        fields = (
                'id', 'username', 'email', 'password', 'first_name', 'last_name', 'individual_unique_number',
                'phone_number',
                'date_of_birth', 'gender')
