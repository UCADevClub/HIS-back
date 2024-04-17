from rest_framework.serializers import ModelSerializer
from user_authentication.models import BaseUser, Address


class AddressCreateSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'country',
            'oblast',
            'city_village',
            'street',
            'house',
            'apartment',
            'postal_code',
        )

    def create(self, validated_data):
        address_instance = Address.objects.create(**validated_data)
        return address_instance


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'country',
            'oblast',
            'city_village',
            'street',
            'house',
            'apartment',
            'postal_code',
        )

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


class BaseUserCreateSerializer(ModelSerializer):
    address = AddressCreateSerializer()

    class Meta:
        model = BaseUser
        fields = (
            'user_id',
            'nationality',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'date_of_birth',
            'gender',
            'phone_number',
            'address',
        )

    def create(self, validated_data):
        base_user_instance = BaseUser.objects.create_user(**validated_data)
        return base_user_instance


class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = BaseUser
        fields = (
            'user_id',
            'nationality',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'date_of_birth',
            'gender',
            'phone_number',
            'address',
        )

    address = AddressSerializer()

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        address_data = validated_data.pop('address', None)
        address_instance = instance.address
        if address_data:
            address_serializer = AddressSerializer(address_instance,
                                                   data=address_data)
            if address_serializer.is_valid():
                address_serializer.save()
        instance.save()
        return instance
