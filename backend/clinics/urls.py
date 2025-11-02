from rest_framework.routers import DefaultRouter
from .views import ClinicViewSet, NurseAssignmentViewSet

router = DefaultRouter()
router.register(r'clinics', ClinicViewSet, basename='clinic')
router.register(r'nurse-assignments', NurseAssignmentViewSet, basename='nurseassignment')

urlpatterns = router.urls