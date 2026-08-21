from django.contrib import admin

# Register your models here.

from .models import MotherProfile, Message

@admin.register(MotherProfile)
class MotherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'due_date', 'clinic_name', 'phone_number']
    search_fields = ['user__username', 'clinic_name', 'phone_number']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp', 'read']
    list_filter = ['read']
