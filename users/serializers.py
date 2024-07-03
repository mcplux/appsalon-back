from typing import Any, Dict
from rest_framework import serializers
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Token

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        # Verification token
        token = get_random_string(length=32)
        expires_on = timezone.now() + timezone.timedelta(days=1)
        Token.objects.create(user=user, token=token, expires_on=expires_on)
        
        return user

# Custom TokenObtainPairSerializer
class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('Invalid credentials')
        
        if not user.is_verified:
            raise AuthenticationFailed('Account is not verified yet')
        
        return super().validate(attrs)
