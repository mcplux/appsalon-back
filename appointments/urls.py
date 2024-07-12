from django.urls import path
from .views import AppointmentListCreateView, AppointmentRetrieveUpdateDestroy

urlpatterns = [
    path('', AppointmentListCreateView.as_view(), name='appointment-list'),
    path('<int:pk>/', AppointmentRetrieveUpdateDestroy.as_view(), name='appointment-details')
]
