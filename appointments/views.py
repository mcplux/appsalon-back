from django.shortcuts import render
from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from .serializer import AppointmentSerializer
from .models import Appointment

# Create your views here.

class AppointmentListCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return Response({'message': 'Appointment created succesfully'}, status=status.HTTP_201_CREATED)
