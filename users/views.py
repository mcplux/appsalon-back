from django.shortcuts import render
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import generics, status
from rest_framework.response import Response
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
