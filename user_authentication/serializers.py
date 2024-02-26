from rest_framework.serializers import ModelSerializer
from user_authentication.models import BaseUser, Address


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
        fields = '__all__'

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

    class Meta:
        model = Address
        fields = ['street',
                  'city',
                  'state',
                  'postal_code']

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
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
