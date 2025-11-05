from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Tip
from .serializers import TipSerializer

# Create your views here.

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Allows read-only access (GET) to any authenticated user.
    - Allows write access (POST, PUT, DELETE) only to Admins.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests for any logged-in user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Deny write access if user is not an Admin
        return request.user and request.user.role == 'ADMIN'
    
# In tips/views.py

class TipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tips to be viewed or edited.
    """
    serializer_class = TipSerializer
    
    # --- CHANGE THIS LINE ---
    permission_classes = [IsAdminOrReadOnly]
    # Was: permission_classes = [IsNurseOrAdminOrReadOnly]

    def perform_create(self, serializer):
        """
        Automatically set the author of the tip to the logged-in admin.
        (This code stays the same, but now only Admins can run it)
        """
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        - Admins see all approved tips + their own drafts.
        - All other users (Mothers, Nurses) see only approved tips.
        """
        user = self.request.user
        
        if user.is_authenticated and user.role == 'ADMIN':
            return Tip.objects.filter(
                Q(is_approved=True) | Q(author=user)
            ).distinct()
        
        # Mothers and Nurses only see approved tips
        return Tip.objects.filter(is_approved=True)