from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegisterView, VerifyAccountView, LoginView, UserView, UserAppointmentsView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-account/<str:token_str>/', VerifyAccountView.as_view(), name='verify-account'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('user/', UserView.as_view(), name='user'),
    path('user/appointments/', UserAppointmentsView.as_view(), name='user-appointments'),
]
