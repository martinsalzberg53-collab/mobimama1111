from rest_framework import serializers
from clinics.models import Clinic, NurseAssignment


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

class NurseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseAssignment
        fields = ['id', 'nurse', 'clinic']
        read_only_fields = ['id']

    def validate_nurse(self, value):
        """Ensure the assigned user is a nurse."""
        if value.role != 'nurse':
            raise serializers.ValidationError("Assigned user must have the role of 'nurse'.")
        return value
    
    def validate(self, data):
        """Cross-field validation."""
        # Prevent duplicate nurse-clinic assignment
        if NurseAssignment.objects.filter(nurse=data['nurse'], clinic=data['clinic']).exists():
            raise serializers.ValidationError("This nurse is already assigned to the specified clinic.")
        
        # Limit a nurse to max 3 clinics
        nurse = data['nurse']
        if NurseAssignment.objects.filter(nurse=nurse).count() >= 1:
            raise serializers.ValidationError("A nurse cannot be assigned to more than 1 clinics.")
        
        return data