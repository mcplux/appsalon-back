from rest_framework import permissions, generics
from .serializers import ServiceSerializer
from .models import Service

# Create your views here.
class ServiceListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
