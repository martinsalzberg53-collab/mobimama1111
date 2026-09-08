from rest_framework import serializers
from django.contrib.auth import authenticate
import re
from .models import User


class LoginSerializer(serializers.Serializer):
    """
    Serializer for logging in. Uses email instead of username.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

            if user.role == 'NURSE' and not user.email_verified:
                msg = 'Please verify your email before logging in. Check your inbox for the verification code.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data



class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, used for retrieving user details.
    """
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'role',
            'clinic',
            'nmc_pin',
            'phone_number',
            'email_verified',
        )


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    Nurses must provide NMC PIN, phone, hospital, and a student email.
    """
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")
    hospital = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'password2',
            'role',
            'nmc_pin',
            'phone_number',
            'hospital',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'min_length': 8},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        email = value.lower().strip()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return email

    def validate_nmc_pin(self, value):
        if not value or not value.strip():
            return value
        pin = value.strip().upper()
        pattern = r'^[A-Z0-9]{4,20}$'
        if not re.match(pattern, pin):
            raise serializers.ValidationError(
                "Invalid NMC PIN format. Use 4-20 alphanumeric characters (e.g., NMC12345 or NMC-12345)."
            )
        return pin

    def validate_phone_number(self, value):
        if not value or not value.strip():
            return value
        phone = value.strip().replace(' ', '').replace('-', '')
        if not re.match(r'^0[235]\d{8}$', phone):
            raise serializers.ValidationError(
                "Invalid Ghana phone number. Use format: 0XX XXX XXXX (e.g., 0240000000)."
            )
        return phone

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        if data['role'] not in ['MOTHER', 'NURSE']:
            raise serializers.ValidationError({"role": "Invalid role. Must be MOTHER or NURSE."})

        if data['role'] == 'NURSE':
            email = data.get('email', '').lower().strip()
            user_model = User()
            if not user_model.is_student_email(email):
                raise serializers.ValidationError({
                    "email": "Nurses must register with an official student/school email address (e.g., name@school.edu.gh)."
                })

            if not data.get('nmc_pin') or not data['nmc_pin'].strip():
                raise serializers.ValidationError({
                    "nmc_pin": "NMC PIN is required for nurse registration."
                })

            if not data.get('phone_number') or not data['phone_number'].strip():
                raise serializers.ValidationError({
                    "phone_number": "Phone number is required for nurse registration."
                })

            if not data.get('hospital') or not data['hospital'].strip():
                raise serializers.ValidationError({
                    "hospital": "Please select your current hospital."
                })

        return data

    def create(self, validated_data):
        hospital = validated_data.pop('hospital', None)
        nmc_pin = validated_data.pop('nmc_pin', None)
        phone_number = validated_data.pop('phone_number', None)

        email_verified = True if validated_data['role'] == 'MOTHER' else False

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            email_verified=email_verified,
            nmc_pin=nmc_pin,
            phone_number=phone_number,
            clinic=hospital,
        )

        return user