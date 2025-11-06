from django.urls import path
from .views import MotherProfileViewSet, MessageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', MotherProfileViewSet, basename='motherprofile')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = router.urls