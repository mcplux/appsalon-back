from django.urls import path
from .views import UserRegisterView, VerifyAccountView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-account/<str:token_str>/', VerifyAccountView.as_view(), name='verify-account'),
]
