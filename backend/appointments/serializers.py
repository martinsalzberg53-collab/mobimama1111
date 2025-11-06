from rest_framework import serializers
from appointments.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'mother', 'nurse', 'clinic_name', 'date_time', 'reason', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'mother', 'status']  # status controlled by nurse/admin

    def create(self, validated_data):
        """
        Automatically assign the authenticated mother as the appointment's mother.
        """
        request = self.context.get('request')
        if request and hasattr(request.user, 'motherprofile'):
            validated_data['mother'] = request.user.motherprofile
        appointment = Appointment.objects.create(**validated_data)
        return appointment

    def update(self, instance, validated_data):
        """
        Update fields allowed to change. Do not overwrite mother or status.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance