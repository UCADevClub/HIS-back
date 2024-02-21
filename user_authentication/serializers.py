from rest_framework.serializers import ModelSerializer
from user_authentication.models import BaseUser, Address


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


class AddressSerializer(ModelSerializer):

    class Meta:
        model = Address
        fields = ['street',
                  'city',
                  'state',
                  'postal_code']

    def update(self, instance, validated_data):
        instance.street = validated_data.get("street", instance.street)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.postal_code = validated_data.get("postal_code", instance.postal_code)
        instance.save()
        return instance

    def create(self, validated_data):
        return Address(**validated_data)

