from django.contrib import admin

# Register your models here.
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['mother', 'nurse', 'clinic_name', 'date_time', 'status']
    list_filter = ['status', 'clinic_name']
    search_fields = ['mother__user__username', 'nurse__username', 'clinic_name']