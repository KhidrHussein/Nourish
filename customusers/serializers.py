from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    otp_totp_secret_key = serializers.CharField(write_only=True, required=False)

class LoginSerializer(serializers.Serializer):
    username_email = serializers.CharField(max_length=254, label='Username or Email')
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
