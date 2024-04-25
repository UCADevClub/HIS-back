from rest_framework.serializers import (
    ModelSerializer,
)
from hospital.models import (
    Hospital,
    Branch,
    BranchPhoneNumber,
    BranchAddress,
)
from staff.models import Doctor
from staff.serializers import (
    DoctorSerializer,
    PatientManagerSerializer,
    BranchAdministratorSerializer,
    HospitalAdministratorSerializer,
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
    director = DoctorSerializer(required=False)
    Hospital = HospitalAdministratorSerializer()
    doctor = DoctorSerializer(many=True)
    branch_administrator = BranchAdministratorSerializer()
    patient_manager = PatientManagerSerializer()

    class Meta:
        model = Branch
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.get('address')
        address_instance = BranchAddress.objects.create(**address_data)
        phone_numbers_data = validated_data.get('phone_number')
        phone_numbers_instance = [
            BranchPhoneNumber.objects.create(**phone_numbers_data) for phone_numbers_data in phone_numbers_data
        ]
        director_data = validated_data.get('director')

        branch_instance = Branch.objects.create(
            address=address_instance,
            **validated_data,
        )
        branch_instance.phone_number.set(phone_numbers_instance)
        if director_data:
            director_instance = Doctor.objects.create(**director_data)
            branch_instance.directors.set(director_instance)

        return branch_instance

    def update(self, instance, validated_data):
        ...


class HospitalSerializer(ModelSerializer):
    branches = BranchAddressSerializer(many=True)

    class Meta:
        model = Hospital
        fields = "__all__"

    def create(self, validated_data):
        hospital_instance = Hospital.objects.create(**validated_data)
        return hospital_instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.website = validated_data.get('website', instance.website)
        instance.hospital_administrator = validated_data.get('hospital_administrator', instance.hospital_administrator)
        instance.save()

        branches_data = validated_data.get('branches', [])
        for branch_data in branches_data:
            branch_id = branch_data.get('id', None)
            if branch_id:
                branch_instance = Branch.objects.get(id=branch_id)
                branch_instance.address.street_address = branch_data.get('address', {}).get('street_address', branch_instance.address.street_address)
                branch_instance.save()
        return instance
