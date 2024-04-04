from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from authentication.models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number', 'password']

    def validate_password(self, value):
        """
        Validate password complexity.
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Create and return a new CustomUser instance.
        """
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)  # Extract email from validated_data
        validated_data['username'] = email  # Set username to email
        user = CustomUser.objects.create_user(email=email, password=password, **validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number', 'profile_picture']