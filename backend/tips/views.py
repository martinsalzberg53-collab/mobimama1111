from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Tip
from .serializers import TipSerializer

# Create your views here.

class IsNurseOrAdminReadOnly(permissions.BasePermission):
    "permission to allow only nurse or admin to edit"
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return request.user and (request.user.role in ['NURSE','ADMIN'])
    
class TipViewSet(viewsets.ModelViewSet):
    "allows tips to be viewed or edited."

    queryset = Tip.objects.filter(is_approved = True)
    serializer_class = TipSerializer
    permission_classes = [IsNurseOrAdminReadOnly]


    def perform_create(self, serializer):
        "sets the tip author to the logged in user when created"
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """mothers only see approved tips
        = nurses can see unapproved tips"""

        user = self.request.user

        if user.role in ['NURSE', 'ADMIN']:
            #nurses/admin get to see their own approved tips or tips they created
            return Tip.objects.filter (models.Q(is_approved = True) | models.Q(author=user).distinct)
        
        #mothers only see approved tips
        return Tip.objects.filter(is_approved=True)
