from rest_framework import serializers
from mothers.models import MotherProfile, Appointment, Message

class MotherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherProfile
        fields = ['id', 'user', 'due_date', 'clinic_name', 'health_info', 'ai_insights', 'phone_number']
        read_only_fields = ['id', 'ai_insights']

    def create(self, validated_data):
        """Create a MotherProfile instance linked to the requesting user."""
        user = self.context['request'].user
        mother_profile = MotherProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        """Update MotherProfile instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    

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
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'read']
        read_only_fields = ['id', 'timestamp', 'sender']

    def create(self, validated_data):
        """Create a Message instance with the authenticated user as sender."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['sender'] = request.user
        message = Message.objects.create(**validated_data)
        return message
    
    def update(self, instance, validated_data):
        """Update Message instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance