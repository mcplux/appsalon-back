from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from .models import Token

# Create your views here.
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            token = Token.objects.get(user=user)
            url = f'{settings.FRONTEND_URL}/auth/verify-account/{token.token}' # Frontend verify account url

            # Send email with token
            subject = 'AppSalon - Verify your account'
            html_content = render_to_string('users/verify_account.html', { 'url': url })
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(subject, text_content, 'admin@appsalon.com', [user.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

        except Exception as e:
            print(e)
            user.delete()
            return Response({ 'message': 'An error ocurred, try again later' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        return Response({ 'message': 'User created succesfully' })

class VerifyAccountView(APIView):
    def get(self, request, token_str):
        token = get_object_or_404(Token, token=token_str)
        user = token.user

        # If token is expired and user is not verified, delete user
        if token.expires_on < timezone.now():
            if not user.is_verified:
                user.delete()
            return Response({ 'message': 'Token expired' }, status=status.HTTP_400_BAD_REQUEST)

        # If user is already verified, return error
        if user.is_verified:
            return Response({ 'message': 'Account already verified' }, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()
        token.delete()

        return Response({ 'message': 'Account verified succesfully' })
