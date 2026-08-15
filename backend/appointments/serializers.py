from rest_framework import serializers
from appointments.models import Appointment
from clinics.models import Clinic
from mothers.models import MotherProfile
from users.models import User


class AppointmentSerializer(serializers.ModelSerializer):
    mother = serializers.PrimaryKeyRelatedField(
        queryset=MotherProfile.objects.all(), required=False
    )
    nurse = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role__iexact='NURSE'), required=False, allow_null=True
    )
    clinic_name = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Appointment
        fields = ['id', 'mother', 'nurse', 'clinic_name', 'date_time', 'reason', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        role = getattr(user, 'role', None)
        if isinstance(role, str):
            role = role.upper()

        if role == 'MOTHER':
            profile, _ = MotherProfile.objects.get_or_create(user=user)
            validated_data['mother'] = profile

        elif role == 'NURSE':
            if 'mother' not in validated_data:
                raise serializers.ValidationError({'mother': 'Mother profile ID is required for nurse booking.'})
            validated_data['nurse'] = user

        appointment = Appointment.objects.create(**validated_data)
        return appointment

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance