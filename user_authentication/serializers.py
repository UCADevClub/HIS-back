from rest_framework.serializers import ModelSerializer
from djoser.serializers import UserCreateSerializer
from user_authentication.models import BaseUser, Address


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = BaseUser
        fields = ['inn', 'email', 'first_name', 'last_name']


class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance

    def create(self, validated_data):
        base_user = BaseUser(**validated_data)
        base_user.objects.create_user()
        base_user.save()
        return base_user


class AddressSerializer(ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.country = validated_data.get("country", instance.country)
        instance.oblast = validated_data.get("oblast", instance.oblast)
        instance.city_village = validated_data.get("city_village", instance.city_village)
        instance.street = validated_data.get("street", instance.street)
        instance.house = validated_data.get("house", instance.house)
        instance.apartment = validated_data.get("apartment", instance.apartment)
        instance.postal_code = validated_data.get("postal_code", instance.postal_code)
        instance.save()
        return instance

    def create(self, validated_data):
        address = Address(**validated_data)
        address.save()
        return address

