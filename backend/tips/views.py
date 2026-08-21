from django.shortcuts import render
from django.db.models import Q

from rest_framework import viewsets, permissions

from .models import Tip
from .serializers import TipSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    - Authenticated users can read tips.
    - Only ADMIN users can create, update or delete tips.
    """

    def has_permission(self, request, view):
        # Allow GET, HEAD and OPTIONS for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return (
                request.user
                and request.user.is_authenticated
            )

        # Only ADMIN can modify tips
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


class TipViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing health tips.
    """

    serializer_class = TipSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user

        # Admin sees approved tips and their own drafts
        if (
            user.is_authenticated
            and user.role == "ADMIN"
        ):
            return Tip.objects.filter(
                Q(is_approved=True) | Q(author=user)
            ).distinct()

        # Everyone else only sees approved tips
        return Tip.objects.filter(is_approved=True)