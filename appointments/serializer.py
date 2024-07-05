from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'user', 'date', 'time', 'total_amount', 'services')
        read_only_fields = ('id', 'user')

