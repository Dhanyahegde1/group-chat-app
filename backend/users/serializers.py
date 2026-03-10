# Import serializer utilities from Django REST Framework
from rest_framework import serializers

# Import the custom User model
from .models import User

# Import Django password validation system
from django.contrib.auth.password_validation import validate_password

# Import validation error class
from django.core.exceptions import ValidationError


# ---------------------------------------------------
# Serializer for User Registration
# ---------------------------------------------------
# This serializer converts JSON request data into a User object
# and handles validation before saving to the database
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        # Model used for serialization
        model = User

        # Fields allowed during registration
        fields = ['username', 'email', 'password']

        # Password should not be returned in API responses
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # ---------------------------------------------------
    # Password Validation
    # ---------------------------------------------------
    # Uses Django's built-in password validation rules
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    # ---------------------------------------------------
    # Create User
    # ---------------------------------------------------
    # Creates a new user using Django's create_user method
    # This automatically hashes the password
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user