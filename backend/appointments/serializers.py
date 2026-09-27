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
    mother_name = serializers.SerializerMethodField()
    nurse_name = serializers.SerializerMethodField()
    nurse_details = serializers.SerializerMethodField()
    clinic_display = serializers.SerializerMethodField()
    mother_summary = serializers.SerializerMethodField()

    def get_mother_name(self, obj):
        if obj.mother and obj.mother.user:
            first = obj.mother.user.first_name or ''
            last = obj.mother.user.last_name or ''
            return f"{first} {last}".strip() or obj.mother.user.email
        return ''

    def get_nurse_name(self, obj):
        if obj.nurse:
            first = obj.nurse.first_name or ''
            last = obj.nurse.last_name or ''
            return f"{first} {last}".strip()
        return ''

    def get_clinic_display(self, obj):
        return obj.clinic_name.name if obj.clinic_name else ''

    def get_nurse_details(self, obj):
        """Credentials the mother can check on arrival at the hospital.

        Only exposed once a nurse has approved the appointment. A nurse
        booking on a mother's behalf fills in ``nurse`` while the status is
        still ``pending``, so the status check is what actually gates this.
        """
        nurse = obj.nurse
        if not nurse or obj.status != 'approved':
            return None
        profile = getattr(nurse, 'nurse_profile', None)
        return {
            'name': self.get_nurse_name(obj),
            # 'PIN' for nurses, 'AIN' for midwives. The number itself is
            # nmc_pin either way, so the type only decides how we label it.
            'registration_type': profile.registration_type if profile else 'PIN',
            'registration_number': nurse.nmc_pin or '',
            'phone_number': nurse.phone_number or '',
        }

    def get_mother_summary(self, obj):
        m = obj.mother
        if not m:
            return None
        return {
            'name': self.get_mother_name(obj),
            'risk_level': m.get_risk_level(),
            'risk_reasons': m.get_risk_reasons(),
            'due_date': m.due_date,
            'phone_number': m.phone_number,
            'indicators': m.health_info or {},
        }

    class Meta:
        model = Appointment
        fields = ['id', 'mother', 'nurse', 'clinic_name', 'date_time', 'reason', 'status', 'created_at', 'updated_at', 'mother_name', 'nurse_name', 'nurse_details', 'clinic_display', 'mother_summary']
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