from django.db import models
from services.models import Service
from users.models import User

# Create your models here.
class Appointment(models.Model):
    services = models.ManyToManyField(Service, related_name='appointments')
    date = models.DateTimeField()
    time = models.CharField(max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')

    def __str__(self):
        return f'{self.user.first_name} - {self.date} - {self.time}'
