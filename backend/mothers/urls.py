from django.urls import path
from .views import mother_dashboard, nurse_dashboard

urlpatterns = [
    path('mother/', mother_dashboard),
    path('nurse/', nurse_dashboard),
]
