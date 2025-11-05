
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipViewSet

router = DefaultRouter()
router.register(r'tips', TipViewSet, basename='tip')

urlpatterns = router.urls