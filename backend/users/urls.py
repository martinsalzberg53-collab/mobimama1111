from django.urls import path
from .views import RegisterView, CustomLoginView, UserProfileView, VerifyOTPView, ResendOTPView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', CustomLoginView.as_view(), name='auth-login'),
    path('profile/', UserProfileView.as_view(), name='auth-profile'),
    path('verify-otp/', VerifyOTPView.as_view(), name='auth-verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='auth-resend-otp'),
]