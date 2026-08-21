from rest_framework.routers import DefaultRouter
from .views import ClinicViewSet, NurseAssignmentViewSet, NurseProfileViewSet

router = DefaultRouter()
router.register(r'clinics', ClinicViewSet, basename='clinic')
router.register(r'nurse-assignments', NurseAssignmentViewSet, basename='nurseassignment')
router.register(r'nurse-profiles', NurseProfileViewSet, basename='nurseprofile')

urlpatterns = router.urls