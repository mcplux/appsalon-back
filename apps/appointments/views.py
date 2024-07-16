from django.shortcuts import render
from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from .serializer import AppointmentSerializer, AppointmentDetailSerializer
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

class AppointmentRetrieveUpdateDestroyView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Get appointment by pk and user
    def get_object(self, pk, user):
        try:
            return Appointment.objects.get(pk=pk, user=user)
        except Appointment.DoesNotExist:
            return None

    # Retrieve
    def get(self, request, pk):
        # Verify if the appointment exists
        appointment = self.get_object(pk, request.user)
        if appointment is None:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Return appointment details
        serializer = AppointmentDetailSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update
    def put(self, request, pk):
        # Verify if the appointment exists
        appointment = self.get_object(pk, request.user)
        if appointment is None:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verify is the request is valid
        serializer = AppointmentSerializer(appointment, data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save appointment
        serializer.save()
        return Response({'message': 'Appointment updated successfully'}, status=status.HTTP_200_OK)

    # Delete
    def delete(self, request, pk):
        # Verify if the appointment exists
        appointment = self.get_object(pk, request.user)
        if appointment is None:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete appointment
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
