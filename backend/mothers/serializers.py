from rest_framework import serializers
from mothers.models import MotherProfile, Message
from users.serializers import UserSerializer
from users.models import User

class MotherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    assigned_nurse = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role__iexact='NURSE'),
        required=False, allow_null=True
    )
    assigned_nurse_name = serializers.SerializerMethodField()
    risk_level = serializers.SerializerMethodField()
    risk_reasons = serializers.SerializerMethodField()

    class Meta:
        model = MotherProfile
        fields = ['id', 'user', 'assigned_nurse', 'assigned_nurse_name', 'due_date', 'clinic_name', 'health_info', 'ai_insights', 'phone_number', 'risk_level', 'risk_reasons']
        read_only_fields = ['id', 'ai_insights', 'risk_level', 'risk_reasons', 'user', 'assigned_nurse_name']

    def get_assigned_nurse_name(self, instance):
        if instance.assigned_nurse:
            first = instance.assigned_nurse.first_name or ''
            last = instance.assigned_nurse.last_name or ''
            return f"{first} {last}".strip() or instance.assigned_nurse.email
        return ''

    def get_risk_level(self, instance):
        return instance.get_risk_level()

    def get_risk_reasons(self, instance):
        return instance.get_risk_reasons()

    def create(self, validated_data):
        """Create a MotherProfile instance linked to the requesting user."""
        user = self.context['request'].user
        mother_profile = MotherProfile.objects.create(user=user, **validated_data)
        return mother_profile

    def update(self, instance, validated_data):
        """Update MotherProfile instance."""
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