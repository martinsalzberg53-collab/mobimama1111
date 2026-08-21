from django.urls import path
from .views import RegisterView, CustomLoginView, UserProfileView

urlpatterns = [
    # e.g., POST /api/users/register/
    path('register/', RegisterView.as_view(), name='auth-register'),
    
    # e.g., POST /api/users/login/
    path('login/', CustomLoginView.as_view(), name='auth-login'),
    
    # e.g., GET /api/users/profile/
    path('profile/', UserProfileView.as_view(), name='auth-profile'),
]