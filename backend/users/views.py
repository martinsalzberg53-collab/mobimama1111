from rest_framework import generics, permissions, status
import sys
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.conf import settings
from django.http import FileResponse, Http404
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .models import User
from .email_utils import send_otp_email
from .license_verify import verify_license_content
from clinics.models import NurseProfile


class RegisterView(generics.CreateAPIView):
    """
    API view for registering a new user.
    Nurses receive an OTP email for verification.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()

            if user.role == 'NURSE':
                self._review_license(user)
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
        except Exception:
            import traceback
            return Response({
                "debug_error": str(sys.exc_info()[1]),
                "debug_traceback": traceback.format_exc(),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _review_license(self, user):
        """Attach OCR result from the uploaded license; fall back to manual review."""
        profile = NurseProfile.objects.filter(user=user).first()
        if not profile or not profile.license_file:
            return

        content = None
        try:
            with profile.license_file.open('rb') as fh:
                content = fh.read()
        except Exception:
            content = None

        if not content:
            profile.license_status = 'PENDING'
            profile.license_review_note = 'License uploaded; awaiting manual admin review (file could not be read for AI review).'
            profile.save(update_fields=['license_status', 'license_review_note'])
            return

        result = verify_license_content(content, profile.license_file.name)

        if result.get('success') and result.get('data', {}).get('is_valid'):
            profile.license_status = 'APPROVED'
            profile.license_review_note = 'Auto-verified by AI OCR review.'
        else:
            profile.license_status = 'PENDING'
            reason = result.get('error') or result.get('data', {}).get('notes') or 'no valid license detected'
            profile.license_review_note = f'Awaiting manual admin review. AI OCR: {reason}'

        profile.license_extracted = result.get('data', {})
        profile.save(update_fields=['license_status', 'license_review_note', 'license_extracted'])


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

        try:
            user.generate_otp()
            send_otp_email(user.email, user.otp_code, user.first_name)
            return Response({
                "message": "A new verification code has been sent to your email.",
            }, status=status.HTTP_200_OK)
        except Exception:
            import traceback
            return Response({
                "debug_error": str(sys.exc_info()[1]),
                "debug_traceback": traceback.format_exc(),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class LicenseFileView(APIView):
    """
    Serve an uploaded NMC license file to its owner nurse or any staff member
    (used by the admin review). Blocks path traversal.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, filepath):
        from clinics.models import NurseProfile

        media_root = settings.MEDIA_ROOT.resolve()
        target = (media_root / filepath).resolve()

        if not str(target).startswith(str(media_root)):
            raise Http404

        profile = None
        try:
            profile = NurseProfile.objects.select_related('user').filter(license_file=filepath).first()
        except Exception:
            profile = None

        owner_ok = profile is not None and request.user.is_authenticated and request.user == profile.user
        if not (request.user.is_staff or owner_ok):
            return Response({"error": "Not authorized to view this file."}, status=status.HTTP_403_FORBIDDEN)

        if not target.exists() or not target.is_file():
            raise Http404

        try:
            return FileResponse(open(target, 'rb'))
        except Exception:
            raise Http404