from rest_framework import viewsets, permissions, status, serializers
from .models import MotherProfile, Message
from .serializers import MotherProfileSerializer, MessageSerializer
from rest_framework.response import Response
from users.models import User
from rest_framework.decorators import action


class MotherProfileViewSet(viewsets.ModelViewSet):

    """API endpoint for MotherProfile CRUD operations."""
    serializer_class = MotherProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return the MotherProfile for the authenticated user."""

        user = self.request.user
        if user.role == 'mother':
            return MotherProfile.objects.filter(user=user)
        return MotherProfile.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'motherprofile'):
            return Response({'detail': 'MotherProfile already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    


class MessageViewSet(viewsets.ModelViewSet):
    """API endpoint for Message CRUD operations."""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return Messages involving the authenticated user."""
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
    
    def perform_create(self, serializer):
        """Automatically assign the authenticated user as the sender."""
        user = self.request.user
        serializer.save(sender=user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Custom action to mark a message as read."""
        message = self.get_object()
        if message.receiver != request.user:
            return Response({'error': 'Only the reciever can mark as read'}, status=status.HTTP_403_FORBIDDEN)
        message.read = True
        message.save()
        serializer = self.get_serializer(message)
        return Response(serializer.data)