from rest_framework.serializers import (
    ModelSerializer,
)
from hospital.models import (
    Hospital,
    Branch,
    BranchPhoneNumber,
    BranchAddress,
)
from staff.serializers import (
    DoctorSerializer,
)


class PhoneNumberSerializer(ModelSerializer):

    class Meta:
        model = BranchPhoneNumber
        fields = (
            'phone_number',
        )

    def create(self, validated_data):
        instance = BranchPhoneNumber.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance):
        instance.delete()


class BranchAddressSerializer(ModelSerializer):

    class Meta:
        model = BranchAddress
        fields = (
            'street_address',
            'building_number',
            'city',
            'state',
            'postal_code',
            'country',
        )

    def create(self, validated_data):
        instance = BranchAddress.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.street_address = validated_data.get('street_address', instance.street_address)
        instance.building_number = validated_data.get('building_number', instance.building_number)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance):
        instance.delete()


class BranchSerializer(ModelSerializer):
    address = BranchAddressSerializer()
    phone_number = PhoneNumberSerializer(many=True)
    director = DoctorSerializer()

    class Meta:
        model = Branch
        fields = (
            ''
        )


class HospitalSerializer(ModelSerializer):
    branches = BranchAddressSerializer(many=True)

    class Meta:
        model = Hospital
        fields = (
            ''
        )

