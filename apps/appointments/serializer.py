from rest_framework import serializers
from .models import Appointment
from apps.services.serializers import ServiceSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'user', 'date', 'time', 'total_amount', 'services')
        read_only_fields = ('id', 'user')

class AppointmentDetailSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = Appointment
        fields = ('id', 'user', 'date', 'time', 'total_amount', 'services')
        read_only_fields = ('id', 'user')
