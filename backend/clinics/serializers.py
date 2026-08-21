from rest_framework import serializers
from clinics.models import Clinic, NurseAssignment
from users.models import User


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address', 'phone_number']
        read_only_fields = ['id']
    
    def validate_name(self, value):
        """Ensure clinic name is unique."""
        if Clinic.objects.filter(name=value).exists():
            raise serializers.ValidationError("Clinic with this name already exists.")
        return value

class NurseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseAssignment
        fields = ['id', 'nurse', 'clinic', 'qualifications', 'phone_number']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """Create a NurseProfile instance."""
        nurse_assignment = NurseAssignment.objects.create(**validated_data)
        return nurse_assignment
    
    def update(self, instance, validated_data):
        """Update NurseProfile instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class NurseAssignmentSerializer(serializers.ModelSerializer):
    nurse = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = NurseAssignment
        fields = ['id', 'nurse', 'clinic']
        read_only_fields = ['id']

    def validate_nurse(self, value):
        """Ensure the assigned user is a nurse."""
        if value.role.upper() != 'NURSE':
            raise serializers.ValidationError("Assigned user must have the role of 'NURSE'.")
        return value

    def validate(self, data):
        """Cross-field validation."""
        instance = self.instance
        nurse = data.get('nurse')
        clinic = data.get('clinic')

        if nurse and clinic:
            # Prevent duplicate nurse-clinic assignment
            qs = NurseAssignment.objects.filter(nurse=nurse, clinic=clinic)
            if instance is not None:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This nurse is already assigned to the specified clinic.")

            # Limit a nurse to 1 clinic
            other = NurseAssignment.objects.filter(nurse=nurse)
            if instance is not None:
                other = other.exclude(pk=instance.pk)
            if other.count() >= 1:
                raise serializers.ValidationError("A nurse cannot be assigned to more than 1 clinic.")

        return data