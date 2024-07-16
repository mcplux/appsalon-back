from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegisterView, VerifyAccountView, LoginView, UserView, UserAppointmentsView

@api_view(['GET'])
def auth_root(request, format=None):
    return Response({
        'register': reverse('register', request=request, format=format),
        'verify-account': reverse('verify-account', args=[':token'], request=request, format=format),
        'login': reverse('login', request=request, format=format),
        'refresh-token': reverse('refresh-token', request=request, format=format),
        'user': reverse('user', request=request, format=format),
        'user-appointments': reverse('user-appointments', request=request, format=format),
    })

urlpatterns = [
    path('', auth_root, name='auth-root'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-account/<str:token_str>/', VerifyAccountView.as_view(), name='verify-account'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('user/', UserView.as_view(), name='user'),
    path('user/appointments/', UserAppointmentsView.as_view(), name='user-appointments'),
]
