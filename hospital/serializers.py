from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    IntegerField,
    CharField,
)
from hospital.models import (
    Department,
    Hospital,
    Branch,
    BranchPhoneNumber,
    BranchAddress,
)
from staff.models import (
    BranchAdministrator,
    Doctor,
    HospitalAdministrator,
    PatientManager
)
from staff.serializers import (
    DoctorSerializer,
    PatientManagerSerializer,
    BranchAdministratorSerializer,
    HospitalAdministratorSerializer,
)


class PhoneNumberSerializer(ModelSerializer):
    class Meta:
        model = BranchPhoneNumber
        fields = "__all__"

    def create(self, validated_data):
        instance = BranchPhoneNumber.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', )
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance):
        instance.delete()


class BranchAddressSerializer(ModelSerializer):
    class Meta:
        model = BranchAddress
        fields = "__all__"

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


class HospitalSerializer(ModelSerializer):
    hospital_administrator = HospitalAdministratorSerializer(required=False)
    hospital_administrator_id = CharField(required=False)

    class Meta:
        model = Hospital
        fields = (
            'name',
            'description',
            'website',
            'hospital_administrator',
            'hospital_administrator_id',
        )

    def create(self, validated_data):
        hospital_administrator_data = validated_data.pop('hospital_administrator', None)
        hospital_administrator_id = validated_data.pop('hospital_administrator_id', None)
        if hospital_administrator_data:
            validated_data['hospital_administrator'] = HospitalAdministrator.objects.create_hospital_administrator(
                **hospital_administrator_data
            )
        else:
            validated_data['hospital_administrator'] = HospitalAdministrator.objects.get(
                user_id=hospital_administrator_id
            )
        hospital_instance = Hospital.objects.create(
            **validated_data,
        )
        return hospital_instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', None)
        instance.description = validated_data.get('description', None)
        instance.website = validated_data.get('website', None)
        hospital_administrator_data = validated_data.get('hospital_administrator', None)
        if hospital_administrator_data:
            hospital_administrator_instance = instance.hospital_administrator
            for attr, value in hospital_administrator_data.items():
                setattr(hospital_administrator_instance, attr, value)
            hospital_administrator_instance.save()
        instance.save()
        return instance


class BranchSerializer(ModelSerializer):
    address = BranchAddressSerializer()
    phone_numbers = PhoneNumberSerializer(many=True, required=False)
    director = DoctorSerializer(required=False)
    doctors = DoctorSerializer(many=True, required=False)
    branch_administrator = BranchAdministratorSerializer(required=False)
    patient_manager = PatientManagerSerializer(required=False)
    hospital_id = IntegerField(write_only=True)

    class Meta:
        model = Branch
        fields = (
            'id',
            'name',
            'email',
            'website',
            'address',
            'phone_numbers',
            'director',
            'doctors',
            'branch_administrator',
            'patient_manager',
            'hospital_id',
        )

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        phone_numbers_data = validated_data.pop('phone_numbers', None)
        director_data = validated_data.pop('director', None)
        hospital_id = validated_data.pop('hospital_id', None)
        doctors_data = validated_data.pop('doctors', [])
        branch_administrator_data = validated_data.pop('branch_administrator', None)
        patient_manager_data = validated_data.pop('patient_manager', None)

        address_instance = BranchAddress.objects.create(**address_data)
        hospital_instance = Hospital.objects.get(id=hospital_id)
        branch_instance = Branch.objects.create(
            address=address_instance,
            hospital=hospital_instance,
            **validated_data,
        )
        if phone_numbers_data:
            phone_numbers_instances = [BranchPhoneNumber.objects.create(**data) for data in phone_numbers_data]
            branch_instance.phone_numbers.set(phone_numbers_instances)

        if director_data:
            director_instance = Doctor.objects.create(**director_data)
            branch_instance.director = director_instance

        branch_instance.doctors.set([Doctor.objects.create(**data) for data in doctors_data])

        if branch_administrator_data:
            branch_administrator_instance = BranchAdministrator.objects.create(**branch_administrator_data)
            branch_instance.branch_administrator = branch_administrator_instance

        if patient_manager_data:
            patient_manager_instance = PatientManager.objects.create(**patient_manager_data)
            branch_instance.patient_manager = patient_manager_instance

        return branch_instance

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        phone_numbers_data = validated_data.pop('phone_numbers', None)
        director_data = validated_data.pop('director', None)
        hospital_data = validated_data.pop('hospital', None)
        doctors_data = validated_data.pop('doctors', None)
        branch_administrator_data = validated_data.pop('branch_administrator', None)
        patient_manager_data = validated_data.pop('patient_manager', None)

        if address_data:
            address_serializer = BranchAddressSerializer(instance.address, data=address_data)
            if address_serializer.is_valid():
                address_serializer.save()

        if phone_numbers_data:
            phone_numbers_instances = [BranchPhoneNumber.objects.create(**data) for data in phone_numbers_data]
            instance.phone_numbers.set(phone_numbers_instances)

        if director_data:
            director_instance = Doctor.objects.create(**director_data)
            instance.director = director_instance

        if hospital_data:
            hospital_serializer = HospitalSerializer(instance.hospital, data=hospital_data)
            if hospital_serializer.is_valid():
                hospital_serializer.save()

        if doctors_data:
            instance.doctors.clear()
            for data in doctors_data:
                doctor_instance = Doctor.objects.create(**data)
                instance.doctors.add(doctor_instance)

        if branch_administrator_data:
            if instance.branch_administrator:
                # Update existing branch administrator
                branch_administrator_serializer = BranchAdministratorSerializer(instance.branch_administrator,
                                                                                data=branch_administrator_data)
            else:
                # Create new branch administrator
                branch_administrator_serializer = BranchAdministratorSerializer(data=branch_administrator_data)

            if branch_administrator_serializer.is_valid():
                branch_administrator = branch_administrator_serializer.save(branch=instance)
                instance.branch_administrator = branch_administrator
            else:
                raise ValidationError(branch_administrator_serializer.errors)

        if patient_manager_data:
            patient_manager_instance = PatientManager.objects.create(**patient_manager_data)
            instance.patient_manager = patient_manager_instance

        instance.save()
        return instance


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
