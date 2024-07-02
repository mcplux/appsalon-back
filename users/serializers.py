from rest_framework import serializers
from django.utils import timezone
from django.utils.crypto import get_random_string
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
