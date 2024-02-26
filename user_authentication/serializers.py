from rest_framework.serializers import ModelSerializer
from djoser.serializers import UserCreateSerializer, UserSerializer
from user_authentication.models import BaseUser, Address
from django.utils.crypto import get_random_string


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


class BaseUserCreateSerializer(ModelSerializer):
    address = AddressCreateSerializer()

    class Meta:
        model = BaseUser
        fields = (
            'inn',
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
        address_data = validated_data.pop('address')
        address_instance = Address.objects.create(**address_data)
        password = get_random_string(8)
        base_user_instance = BaseUser.objects.create(**validated_data, password=password, address=address_instance)
        return base_user_instance


class BaseUserSerializer(ModelSerializer):
    """
    Serializer for the BaseUser model.

    Attributes:
        Meta:
            model (class): The BaseUser model to be serialized.
            fields (list): List of fields to include in the serialized representation.

    Examples:
        To use this serializer, instantiate it in your views or API endpoints:

        ```python
        serializer = BaseUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        ```

    """
    class Meta:
        model = BaseUser
        fields = (
            'inn',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'date_of_birth',
            'gender',
            'phone_number',
            'address',
        )

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance


class MainBaseUserSerializer(ModelSerializer):

    class Meta:
        fields = (
            'inn',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'password'
        )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.email = validated_data.get('email', instance.email)

        instance.save()

        return instance


class AddressSerializer(ModelSerializer):
<<<<<<< HEAD

    """
    Serializer for the Address model.

    Attributes:
        Meta:
            model (class): The Address model to be serialized.
            fields (list): List of fields to include in the serialized representation.

    Methods:
        create(validated_data): Create a new Address instance with the provided data.
        update(instance, validated_data): Update the fields of an existing Address instance.

    Examples:
        To use this serializer, instantiate it in your views or API endpoints:

        ```python
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        ```

    """

=======
>>>>>>> cf1a8777eb6e838685a1ef4bda499c4024008297
    class Meta:
        model = Address
        fields = '__all__'

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
<<<<<<< HEAD
        primary_address_data = validated_data.pop('primary_address', None)

        if primary_address_data is not None:
            # If primary_address_data is provided, update the existing address or create a new one
            if instance.primary_address:
                # Update the existing address
                address_serializer = AddressSerializer(
                    instance.primary_address, data=primary_address_data, partial=True
                )
                if address_serializer.is_valid():
                    address_serializer.save()
            else:
                # Create a new address
                new_address_serializer = AddressSerializer(data=primary_address_data)
                if new_address_serializer.is_valid():
                    new_address_serializer.save()
                    instance.primary_address = new_address_serializer.instance

        # Update other fields of the main model instance if needed
        instance.save()
        return instance
=======
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
        address = Address(validated_data)
        address.save()
        return address

>>>>>>> cf1a8777eb6e838685a1ef4bda499c4024008297
