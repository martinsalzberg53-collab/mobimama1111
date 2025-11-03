from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import current_user


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #login and access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #refresh token
    path('current_user/', current_user, name='current_user'), #get current user info
]