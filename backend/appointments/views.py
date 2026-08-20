from django.shortcuts import render

from django.db.models import Q
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
from sms.utils import send_appointment_confirmation, send_appointment_approved, send_appointment_cancelled


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
            # Nurses see pending (unassigned) appointments at their clinic to
            # triage, plus appointments for mothers already assigned to them.
            return Appointment.objects.filter(clinic_name__id__in=assigned_clinics).filter(
                Q(mother__assigned_nurse=user) | Q(mother__assigned_nurse__isnull=True)
            )

        return Appointment.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        role = self._normalize_role(getattr(user, 'role', None))

        if role == 'MOTHER':
            if hasattr(user, 'motherprofile'):
                appt = serializer.save(mother=user.motherprofile)
                phone = user.motherprofile.phone_number
                if phone:
                    clinic_name = str(appt.clinic_name) if appt.clinic_name else "your clinic"
                    send_appointment_confirmation(phone, clinic_name, str(appt.date_time))
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
        if appointment.mother and appointment.mother.assigned_nurse and appointment.mother.assigned_nurse != user:
            return Response(
                {'error': 'This mother is already assigned to another nurse.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        appointment.status = 'approved'
        appointment.nurse = user
        if appointment.mother:
            appointment.mother.assigned_nurse = user
            appointment.mother.save(update_fields=['assigned_nurse'])
            phone = appointment.mother.phone_number
            if phone:
                clinic_name = str(appointment.clinic_name) if appointment.clinic_name else "your clinic"
                send_appointment_approved(phone, clinic_name)
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Custom action to reject an appointment (nurse only)."""
        appointment = self.get_object()
        user = request.user
        if self._normalize_role(getattr(user, 'role', None)) != 'NURSE':
            return Response({'error': 'Only nurses can reject appointments.'}, status=status.HTTP_403_FORBIDDEN)
        appointment.status = 'cancelled'
        appointment.save()
        if appointment.mother:
            phone = appointment.mother.phone_number
            if phone:
                send_appointment_cancelled(phone)
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
