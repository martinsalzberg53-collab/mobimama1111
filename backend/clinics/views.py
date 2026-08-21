from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions, serializers
from .models import Clinic, NurseAssignment
from .serializers import ClinicSerializer, NurseAssignmentSerializer


class ClinicViewSet(viewsets.ModelViewSet):
    """API endpoint that allows clinics to be viewed or edited."""
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    
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

    def perform_create(self, serializer):
        '''Nurses create their own assignment; admins can assign on behalf of others.'''
        user = self.request.user
        if self._normalize_role(getattr(user, 'role', None)) != 'ADMIN':
            if NurseAssignment.objects.filter(nurse=user).exists():
                raise serializers.ValidationError(
                    "You already have a clinic assigned. Update it instead of creating a new one."
                )
            serializer.save(nurse=user)
        else:
            serializer.save()