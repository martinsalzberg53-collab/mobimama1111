from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status, serializers
from users.models import User
from rest_framework.decorators import action
from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """API endpoint for Appointment CRUD operations."""
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return Appointments based on user role."""
        user = self.request.user
        if user.role == 'mother':
            """Return appointments for the mother."""
            if hasattr(user, 'motherprofile'):
                return Appointment.objects.filter(mother=user.motherprofile)
            else:
                return Appointment.objects.none()
            
        elif user.role == 'nurse':
            """Return appointments assigned to the nurse."""
            assigned_clinics = user.nurseassignment_set.values_list('clinic', flat=True)
            return Appointment.objects.filter(clinic_name__id__in=assigned_clinics)
        
        else:
            """Admin or other roles see all appointments."""
        return Appointment.objects.all()
    
    def perform_create(self, serializer):
        """Automatically assign the authenticated mother as the appointment's mother."""
        user = self.request.user
        
        if hasattr(user, 'motherprofile'):
            serializer.save(mother=user.motherprofile)
        else:
            raise serializers.ValidationError('You must have a mother profile to create an appointment.')
        
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Custom action to approve an appointment (nurse only)."""
        appointment = self.get_object()
        user = request.user
        if user.role != 'nurse':
            return Response({'error': 'Only nurses can approve appointments.'}, status=status.HTTP_403_FORBIDDEN)
        appointment.status = 'approved'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
        