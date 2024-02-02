from rest_framework.serializers import ModelSerializer
from user_authentication.models import BaseUser, Address


class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'


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

