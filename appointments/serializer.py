from rest_framework import serializers
from .models import Appointment
from services.serializers import ServiceSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = Appointment
        fields = ('id', 'user', 'date', 'time', 'total_amount', 'services')
        read_only_fields = ('id', 'user')

