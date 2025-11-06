from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, used for retrieving user details.
    This is a "read-only" serializer.
    """
    class Meta:
        model = User
        # These are the fields that will be sent to the frontend.
        # Notice the password is NOT here.
        fields = (
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'role', 
            'clinic'
        )

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    This is a "write-only" serializer.
    """
    # We add 'password2' to check for a password confirmation
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")

    class Meta:
        model = User
        fields = (
            'email', 
            'first_name', 
            'last_name', 
            'password', 
            'password2', 
            'role'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'min_length': 8},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, data):
        """
        Check that the two passwords match and the role is valid.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # Security check: only allow 'MOTHER' or 'NURSE' to be created
        # via the public API. 'ADMIN' can only be created via 'createsuperuser'.
        if data['role'] not in ['MOTHER', 'NURSE']:
            raise serializers.ValidationError({"role": "Invalid role. Must be MOTHER or NURSE."})
            
        return data

    def create(self, validated_data):
        """
        Create and return a new user, properly hashing the password.
        """
        # We use our custom 'create_user' manager method
        # which handles password hashing.
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )
        return user