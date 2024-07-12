from django.shortcuts import render
from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from .serializer import AppointmentSerializer
from .models import Appointment

# Create your views here.

class AppointmentListCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        date = request.query_params.get('date')
        if date is None:
            return Response({'error': 'Date is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            appointments = Appointment.objects.filter(date=date)
            serializer = AppointmentSerializer(appointments, many=True)
            response = [
                {
                    'id': appointment['id'],
                    'time': appointment['time'],
                } for appointment in serializer.data
            ]
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Invalid date'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return Response({'message': 'Appointment created succesfully'}, status=status.HTTP_201_CREATED)

class AppointmentRetrieveUpdateDestroy(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        try:
            appointment = Appointment.objects.get(pk=pk, user=user)
            serializer = AppointmentSerializer(appointment)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({'message': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
