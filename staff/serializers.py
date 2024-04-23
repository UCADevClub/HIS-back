from rest_framework.serializers import ModelSerializer
from staff.models import Department, Speciality, Doctor


class SpecialitySerializer(ModelSerializer):
    class Meta:
        model = Speciality
        fields = (
            'position',
            'description',
        )

    def create(self, validated_data):
        instance = Speciality.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.position = validated_data.get('position', instance.position)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance):
        instance.delete()


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            ''
        )


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = (
            'name',
            'description'
        )

