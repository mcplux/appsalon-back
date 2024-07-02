from rest_framework import serializers
from django.utils.crypto import get_random_string
from .models import User, Token

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = get_random_string(length=32)
        Token.objects.create(user=user, token=token)
        return user
