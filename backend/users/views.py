from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer, RegisterSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    """
    API view for registering a new user.
    """
    queryset = User.objects.all()
    # Anyone can access this page (e.g., to sign up)
    permission_classes = (permissions.AllowAny,) 
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create a token for the new user right after they register
        token, created = Token.objects.get_or_create(user=user)
        
        # Return both the new user's data and their token
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

class CustomLoginView(ObtainAuthToken):
    """
    API view for user login.
    This replaces the default login view so we can return
    the user's data along with their token.
    """
    # Anyone can access this page (e.g., to log in)
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        # Try to log the user in
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Get or create a token for them
        token, created = Token.objects.get_or_create(user=user)
        
        # Return the token AND the user's profile data
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the logged-in user's profile.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # This view is protected: only logged-in users can access it
    permission_classes = (permissions.IsAuthenticated,) 

    def get_object(self):
        # This method is a shortcut to get the specific user
        # making the request. No need for a user ID in the URL.
        return self.request.user