from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .models import User
from .email_utils import send_otp_email


class RegisterView(generics.CreateAPIView):
    """
    API view for registering a new user.
    Nurses receive an OTP email for verification.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user.role == 'NURSE':
            user.generate_otp()
            send_otp_email(user.email, user.otp_code, user.first_name)
            return Response({
                "message": "Registration successful. Please check your email for a 6-digit verification code.",
                "email": user.email,
                "requires_verification": True,
            }, status=status.HTTP_201_CREATED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key,
            "requires_verification": False,
        }, status=status.HTTP_201_CREATED)


class VerifyOTPView(APIView):
    """
    Verify nurse's email with OTP code.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        otp = request.data.get('otp', '').strip()

        if not email or not otp:
            return Response(
                {"error": "Email and verification code are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "No account found with this email."},
                status=status.HTTP_404_NOT_FOUND
            )

        success, message = user.verify_otp(otp)

        if not success:
            return Response(
                {"error": message},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": message,
            "user": UserSerializer(user).data,
            "token": token.key,
        }, status=status.HTTP_200_OK)


class ResendOTPView(APIView):
    """
    Resend OTP verification code to nurse's email.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email', '').strip().lower()

        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "No account found with this email."},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.email_verified:
            return Response(
                {"message": "Email is already verified. You can log in."},
                status=status.HTTP_200_OK
            )

        user.generate_otp()
        send_otp_email(user.email, user.otp_code, user.first_name)

        return Response({
            "message": "A new verification code has been sent to your email.",
        }, status=status.HTTP_200_OK)


class CustomLoginView(ObtainAuthToken):
    """
    API view for user login.
    Returns token and user data.
    Nurses must have email_verified=True.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

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
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user