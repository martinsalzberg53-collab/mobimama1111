from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions, serializers
from .models import Clinic, NurseAssignment
from .serializers import ClinicSerializer, NurseAssignmentSerializer


class ClinicViewSet(viewsets.ModelViewSet):
    """API endpoint that allows clinics to be viewed or edited.

    The platform presents the 16 regional hospitals (one per region) to the
    public; the full directory remains available to admin users.
    """
    serializer_class = ClinicSerializer
    
    def get_queryset(self):
        return Clinic.objects.filter(regional=True)
    
    def get_permissions(self):

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
class NurseProfileViewSet(viewsets.ModelViewSet):

    serializer_class = NurseAssignmentSerializer
    permission_classes = [permissions.IsAdminUser]

    def _normalize_role(self, role):
        return role.upper() if isinstance(role, str) else role

    def get_queryset(self):
        user = self.request.user
        if self._normalize_role(getattr(user, 'role', None)) == 'NURSE':
            return NurseAssignment.objects.filter(nurse=user)
        return NurseAssignment.objects.all()

class NurseAssignmentViewSet(viewsets.ModelViewSet):

    serializer_class = NurseAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _normalize_role(self, role):
        return role.upper() if isinstance(role, str) else role

    def get_queryset(self):
        user = self.request.user
        if self._normalize_role(getattr(user, 'role', None)) == 'ADMIN':
            return NurseAssignment.objects.all()
        return NurseAssignment.objects.filter(nurse=user)

    def _is_admin(self):
        return self._normalize_role(getattr(self.request.user, 'role', None)) == 'ADMIN'

    def perform_create(self, serializer):
        '''Nurses create their own assignment; admins can assign on behalf of others.'''
        user = self.request.user
        if not self._is_admin():
            if NurseAssignment.objects.filter(nurse=user).exists():
                raise serializers.ValidationError(
                    "You already have a clinic assigned. Update it instead of creating a new one."
                )
            serializer.save(nurse=user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        '''Only admins may reassign a nurse to a different hospital.'''
        if not self._is_admin():
            raise serializers.ValidationError(
                "Your hospital was set at registration and cannot be changed. Contact an administrator."
            )
        serializer.save()

    def perform_destroy(self, instance):
        '''Only admins may remove a nurse's hospital assignment.'''
        if not self._is_admin():
            raise serializers.ValidationError(
                "Your hospital was set at registration and cannot be changed. Contact an administrator."
            )
        instance.delete()