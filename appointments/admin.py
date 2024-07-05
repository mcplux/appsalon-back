from django.contrib import admin
from .models import Appointment

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'total_amount')
    search_fields = ('user__first_name', 'date', 'time')
    list_filter = ('date', 'time')
    
