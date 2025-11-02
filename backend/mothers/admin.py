from django.contrib import admin

# Register your models here.

from .models import MotherProfile, Appointment, Message

@admin.register(MotherProfile)
class MotherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'due_date', 'clinic_name', 'phone_number']
    search_fields = ['user__username', 'clinic_name', 'phone_number']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['mother', 'nurse', 'clinic_name', 'date_time', 'status']
    list_filter = ['status', 'clinic_name']
    search_fields = ['mother__user__username', 'nurse__username', 'clinic_name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp', 'read']
    list_filter = ['read']
