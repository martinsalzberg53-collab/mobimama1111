from django.shortcuts import render

from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """API endpoint for Appointment CRUD operations."""
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _normalize_role(self, role):
        return role.upper() if isinstance(role, str) else role

    def get_queryset(self):
        """Return Appointments based on user role."""
        user = self.request.user
        role = self._normalize_role(getattr(user, 'role', None))

        if role == 'MOTHER':
            if hasattr(user, 'motherprofile'):
                return Appointment.objects.filter(mother=user.motherprofile)
            return Appointment.objects.none()

        if role == 'NURSE':
            assigned_clinics = user.nurseassignment_set.values_list('clinic', flat=True)
            return Appointment.objects.filter(clinic_name__id__in=assigned_clinics)

        return Appointment.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        role = self._normalize_role(getattr(user, 'role', None))

        if role == 'MOTHER':
            if hasattr(user, 'motherprofile'):
                serializer.save(mother=user.motherprofile)
            else:
                raise serializers.ValidationError('You must have a mother profile to create an appointment.')
        elif role == 'NURSE':
            serializer.save(nurse=user)
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Custom action to approve an appointment (nurse only)."""
        appointment = self.get_object()
        user = request.user
        if self._normalize_role(getattr(user, 'role', None)) != 'NURSE':
            return Response({'error': 'Only nurses can approve appointments.'}, status=status.HTTP_403_FORBIDDEN)
        appointment.status = 'approved'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
