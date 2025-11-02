from django.contrib import admin

# Register your models here.

from .models import Clinic, NurseAssignment

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number')
    search_fields = ('name', 'address', 'phone_number')

@admin.register(NurseAssignment)
class NurseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('nurse', 'clinic')
    search_fields = ('nurse__username', 'clinic__name')